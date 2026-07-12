from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from fastapi import HTTPException, UploadFile
from datetime import datetime, date, timedelta
import os

from app.utils.uploads import (
    validate_upload,
    ALLOWED_DOCUMENT_EXTENSIONS,
    MAX_DOCUMENT_SIZE_BYTES,
)

from app.models.contract import Contract
from app.models.certification import Certification
from app.models.compliance_record import ComplianceRecord
from app.models.vendor import Vendor
from app.schemas.contract import ContractCreate, ContractUpdate
from app.schemas.certification import CertificationCreate, CertificationUpdate
from app.schemas.compliance_record import ComplianceRecordCreate, ComplianceRecordUpdate


def generate_contract_number(db: Session) -> str:
    year = datetime.utcnow().year
    prefix = f"CON-{year}-"
    last = (
        db.query(Contract.contract_number)
        .filter(Contract.contract_number.like(f"{prefix}%"))
        .order_by(Contract.contract_number.desc())
        .first()
    )

    next_seq = 1
    if last and last[0]:
        try:
            next_seq = int(last[0].rsplit("-", 1)[1]) + 1
        except (ValueError, IndexError):
            next_seq = (db.query(func.count(Contract.id)).scalar() or 0) + 1

    while db.query(Contract).filter(Contract.contract_number == f"{prefix}{next_seq:04d}").first():
        next_seq += 1
    return f"{prefix}{next_seq:04d}"


def _store_upload(file: UploadFile, folder: str, vendor_id: int):
    contents = validate_upload(file, ALLOWED_DOCUMENT_EXTENSIONS, MAX_DOCUMENT_SIZE_BYTES)

    upload_dir = os.path.join("static", folder, str(vendor_id))
    os.makedirs(upload_dir, exist_ok=True)

    safe_filename = os.path.basename(file.filename)
    file_path = os.path.join(upload_dir, safe_filename)
    with open(file_path, "wb") as buffer:
        buffer.write(contents)

    return safe_filename, file_path


def create_contract(db: Session, data: ContractCreate, file: UploadFile = None):
    v = db.query(Vendor).filter(Vendor.id == data.vendor_id).first()
    if not v:
        raise HTTPException(status_code=404, detail="Vendor not found")

    con_num = generate_contract_number(db)
    file_name = None
    file_path = None

    if file and file.filename:
        file_name, file_path = _store_upload(file, "contracts", data.vendor_id)

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
    for c in contracts:
        if c.status not in ("Terminated", "Renewed"):
            if c.end_date < today:
                c.status = "Expired"
            elif (c.end_date - today).days <= 30:
                c.status = "Expiring Soon"
    db.commit()
    return contracts


def get_contracts_by_vendor(db: Session, vendor_id: int):
    contracts = db.query(Contract).filter(Contract.vendor_id == vendor_id).all()
    today = date.today()
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

    for key, value in data.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(c, key, value)

    db.commit()
    db.refresh(c)
    return c


def renew_contract(db: Session, contract_id: int, new_end_date: date, new_value: float = None):
    c = get_contract_by_id(db, contract_id)
    if not c:
        raise HTTPException(status_code=404, detail="Contract not found")

    if new_end_date <= date.today():
        raise HTTPException(status_code=400, detail="Renewal end date must be in the future")

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
    if c.status in ("Active", "Expiring Soon"):
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete contract in '{c.status}' status. Terminate or let it expire first."
        )
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


def certification_status(expiry_date: date) -> str:
    today = date.today()
    if expiry_date < today:
        return "Expired"
    if (expiry_date - today).days <= 30:
        return "Expiring Soon"
    return "Active"


def add_certification(db: Session, data: CertificationCreate, file: UploadFile = None):
    vendor = db.query(Vendor).filter(Vendor.id == data.vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")

    if data.expiry_date < data.issue_date:
        raise HTTPException(status_code=400, detail="Expiry date cannot be earlier than the issue date")

    file_name = None
    file_path = None

    if file and file.filename:
        file_name, file_path = _store_upload(file, "certifications", data.vendor_id)

    status = certification_status(data.expiry_date)

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
    for c in certs:
        c.status = certification_status(c.expiry_date)
    db.commit()
    return certs


def get_certification(db: Session, cert_id: int):
    return db.query(Certification).filter(Certification.id == cert_id).first()


def update_certification(db: Session, cert_id: int, data: CertificationUpdate, file: UploadFile = None):
    cert = get_certification(db, cert_id)
    if not cert:
        raise HTTPException(status_code=404, detail="Certification not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(cert, key, value)

    if file and file.filename:
        previous_path = cert.file_path
        cert.file_name, cert.file_path = _store_upload(file, "certifications", cert.vendor_id)
        if previous_path and os.path.normpath(previous_path) != os.path.normpath(cert.file_path):
            try:
                os.remove(previous_path)
            except OSError:
                pass

    if cert.expiry_date and cert.issue_date and cert.expiry_date < cert.issue_date:
        raise HTTPException(status_code=400, detail="Expiry date cannot be earlier than the issue date")

    cert.status = certification_status(cert.expiry_date)
    db.commit()
    db.refresh(cert)
    return cert


def delete_certification(db: Session, cert_id: int):
    c = get_certification(db, cert_id)
    if not c:
        raise HTTPException(status_code=404, detail="Certification not found")

    stored_path = c.file_path
    db.delete(c)
    db.commit()

    if stored_path:
        try:
            os.remove(stored_path)
        except OSError:
            pass

    return {"message": "Certification deleted"}


def get_expiring_certifications(db: Session, days_threshold: int = 90):
    threshold_date = date.today() + timedelta(days=days_threshold)
    certs = db.query(Certification).filter(
        Certification.expiry_date <= threshold_date
    ).order_by(Certification.expiry_date.asc()).all()
    for c in certs:
        c.status = certification_status(c.expiry_date)
    db.commit()
    return certs


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
