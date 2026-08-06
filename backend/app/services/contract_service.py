from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, UploadFile
from datetime import datetime, date, timedelta
import os
import shutil

from app.models.contract import Contract
from app.models.certification import Certification
from app.models.compliance_record import ComplianceRecord
from app.models.vendor import Vendor
from app.schemas.contract import ContractCreate, ContractUpdate
from app.schemas.certification import CertificationCreate, CertificationUpdate
from app.schemas.compliance_record import ComplianceRecordCreate, ComplianceRecordUpdate


def generate_contract_number(db: Session) -> str:
    count = db.query(Contract).count() + 1
    return f"CON-{datetime.utcnow().year}-{count:04d}"


def create_contract(db: Session, data: ContractCreate, file: UploadFile = None):
    v = db.query(Vendor).filter(Vendor.id == data.vendor_id).first()
    if not v:
        raise HTTPException(status_code=404, detail="Vendor not found")

    con_num = generate_contract_number(db)
    file_name = None
    file_path = None

    if file:
        upload_dir = os.path.join("static", "contracts", str(data.vendor_id))
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_name = file.filename

    today = date.today()
    status = data.status or "Active"
    if data.end_date < today:
        status = "Expired"
    elif (data.end_date - today).days <= 30:
        status = "Expiring Soon"

    contract = Contract(
        contract_number=con_num,
        contract_title=data.contract_title,
        vendor_id=data.vendor_id,
        vendor_name=v.company_name,
        contract_type=data.contract_type or "Master Agreement",
        procurement_category=data.procurement_category or v.category,
        start_date=data.start_date,
        end_date=data.end_date,
        contract_value=data.contract_value,
        payment_terms=data.payment_terms or "Net 30",
        sla_details=data.sla_details,
        warranty_details=data.warranty_details,
        responsible_manager=data.responsible_manager,
        status=status,
        document_name=file_name,
        document_path=file_path
    )

    try:
        db.add(contract)
        db.commit()
        db.refresh(contract)
        return contract
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def get_all_contracts(db: Session):
    contracts = db.query(Contract).all()
    today = date.today()
    # Update contract statuses on retrieval
    for c in contracts:
        if c.status not in ("Terminated", "Renewed"):
            if c.end_date < today:
                c.status = "Expired"
            elif (c.end_date - today).days <= 30:
                c.status = "Expiring Soon"
    db.commit()
    return contracts


def get_contract_by_id(db: Session, contract_id: int):
    c = db.query(Contract).filter(Contract.id == contract_id).first()
    if c:
        today = date.today()
        if c.status not in ("Terminated", "Renewed"):
            if c.end_date < today:
                c.status = "Expired"
            elif (c.end_date - today).days <= 30:
                c.status = "Expiring Soon"
            db.commit()
    return c


def update_contract(db: Session, contract_id: int, data: ContractUpdate):
    c = get_contract_by_id(db, contract_id)
    if not c:
        raise HTTPException(status_code=404, detail="Contract not found")

    for key, value in data.dict(exclude_unset=True).items():
        if value is not None:
            setattr(c, key, value)

    db.commit()
    db.refresh(c)
    return c


def renew_contract(db: Session, contract_id: int, new_end_date: date, new_value: float = None):
    c = get_contract_by_id(db, contract_id)
    if not c:
        raise HTTPException(status_code=404, detail="Contract not found")

    c.end_date = new_end_date
    if new_value:
        c.contract_value = new_value
    c.status = "Active"
    c.renewal_count += 1
    c.last_renewed_at = datetime.utcnow()

    db.commit()
    db.refresh(c)
    return c


def delete_contract(db: Session, contract_id: int):
    c = get_contract_by_id(db, contract_id)
    if not c:
        raise HTTPException(status_code=404, detail="Contract not found")
    db.delete(c)
    db.commit()
    return {"message": "Contract deleted successfully"}


def get_expiring_contracts(db: Session, days_threshold: int = 90):
    today = date.today()
    threshold_date = today + timedelta(days=days_threshold)
    return db.query(Contract).filter(
        Contract.end_date <= threshold_date,
        Contract.status.in_(["Active", "Expiring Soon", "Expired"])
    ).all()


# Certifications
def add_certification(db: Session, data: CertificationCreate, file: UploadFile = None):
    file_name = None
    file_path = None

    if file:
        upload_dir = os.path.join("static", "certifications", str(data.vendor_id))
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_name = file.filename

    today = date.today()
    status = "Active"
    if data.expiry_date < today:
        status = "Expired"
    elif (data.expiry_date - today).days <= 30:
        status = "Expiring Soon"

    cert = Certification(
        vendor_id=data.vendor_id,
        certification_name=data.certification_name,
        certificate_number=data.certificate_number,
        issuing_authority=data.issuing_authority,
        issue_date=data.issue_date,
        expiry_date=data.expiry_date,
        status=status,
        file_name=file_name,
        file_path=file_path
    )
    db.add(cert)
    db.commit()
    db.refresh(cert)
    return cert


def get_vendor_certifications(db: Session, vendor_id: int):
    certs = db.query(Certification).filter(Certification.vendor_id == vendor_id).all()
    today = date.today()
    for c in certs:
        if c.expiry_date < today:
            c.status = "Expired"
        elif (c.expiry_date - today).days <= 30:
            c.status = "Expiring Soon"
    db.commit()
    return certs


def delete_certification(db: Session, cert_id: int):
    c = db.query(Certification).filter(Certification.id == cert_id).first()
    if c:
        db.delete(c)
        db.commit()
    return {"message": "Certification deleted"}


# Compliance
def record_compliance(db: Session, data: ComplianceRecordCreate):
    rec = ComplianceRecord(
        vendor_id=data.vendor_id,
        compliance_type=data.compliance_type,
        status=data.status or "Pending Verification",
        verified_by=data.verified_by,
        verification_date=data.verification_date or date.today(),
        expiry_date=data.expiry_date,
        remarks=data.remarks
    )
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec


def get_vendor_compliance(db: Session, vendor_id: int):
    return db.query(ComplianceRecord).filter(ComplianceRecord.vendor_id == vendor_id).all()


def update_compliance_status(db: Session, compliance_id: int, status: str, verified_by: str = None, remarks: str = None):
    rec = db.query(ComplianceRecord).filter(ComplianceRecord.id == compliance_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Compliance record not found")

    rec.status = status
    if verified_by:
        rec.verified_by = verified_by
        rec.verification_date = date.today()
    if remarks:
        rec.remarks = remarks

    db.commit()
    db.refresh(rec)
    return rec


def get_compliance_dashboard(db: Session):
    total_records = db.query(ComplianceRecord).count()
    compliant = db.query(ComplianceRecord).filter(ComplianceRecord.status == "Compliant").count()
    pending = db.query(ComplianceRecord).filter(ComplianceRecord.status == "Pending Verification").count()
    non_compliant = db.query(ComplianceRecord).filter(ComplianceRecord.status == "Non-Compliant").count()

    compliance_percentage = round((compliant / total_records * 100), 2) if total_records > 0 else 100.0

    return {
        "total_compliance_records": total_records,
        "compliant_count": compliant,
        "pending_verification_count": pending,
        "non_compliant_count": non_compliant,
        "compliance_percentage": compliance_percentage
    }
