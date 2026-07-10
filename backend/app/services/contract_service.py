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


def _pending_contract_service_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_contract_service_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_contract_service_rows_2(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_contract_service_totals_2(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_contract_service_rows_3(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_contract_service_totals_3(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_contract_service_rows_4(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_contract_service_totals_4(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_contract_service_rows_5(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_contract_service_totals_5(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_contract_service_rows_6(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_contract_service_totals_6(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals
