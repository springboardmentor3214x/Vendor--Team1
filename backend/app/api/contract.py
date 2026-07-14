from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.database.connection import get_db
from app.schemas.contract import ContractCreate, ContractUpdate, ContractResponse
from app.schemas.certification import CertificationCreate, CertificationUpdate, CertificationResponse
from app.schemas.compliance_record import ComplianceRecordCreate, ComplianceRecordResponse
from app.services import contract_service
from app.core.dependencies import get_current_user, role_required
from app.core.roles import Roles, INTERNAL_ROLES
from app.core.vendor_scope import assert_owns, restrict_to_vendor
from app.models.user import User

router = APIRouter(prefix="/contracts", tags=["Contracts & Compliance"])

@router.post("/", response_model=ContractResponse, status_code=201)
def create_contract(
    data: ContractCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN, Roles.PROCUREMENT_MANAGER]))
):
    return contract_service.create_contract(db, data)

@router.post("/upload", response_model=ContractResponse, status_code=201)
async def create_contract_with_file(
    contract_title: str = Form(...),
    vendor_id: int = Form(...),
    contract_type: Optional[str] = Form("Master Agreement"),
    procurement_category: Optional[str] = Form(None),
    start_date: date = Form(...),
    end_date: date = Form(...),
    contract_value: float = Form(...),
    payment_terms: Optional[str] = Form("Net 30"),
    sla_details: Optional[str] = Form(None),
    warranty_details: Optional[str] = Form(None),
    responsible_manager: Optional[str] = Form(None),
    status: Optional[str] = Form("Active"),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN, Roles.PROCUREMENT_MANAGER]))
):
    c_data = ContractCreate(
        contract_title=contract_title,
        vendor_id=vendor_id,
        contract_type=contract_type,
        procurement_category=procurement_category,
        start_date=start_date,
        end_date=end_date,
        contract_value=contract_value,
        payment_terms=payment_terms,
        sla_details=sla_details,
        warranty_details=warranty_details,
        responsible_manager=responsible_manager,
        status=status
    )
    return contract_service.create_contract(db, c_data, file=file)

@router.get("/", response_model=List[ContractResponse])
def list_contracts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == Roles.VENDOR:
        from app.models.vendor import Vendor
        from sqlalchemy import func
        vendor = db.query(Vendor).filter(func.lower(Vendor.email) == current_user.email.lower()).first()
        if vendor:
            return contract_service.get_contracts_by_vendor(db, vendor.id)
        return []
    return contract_service.get_all_contracts(db)

@router.get("/expiring", response_model=List[ContractResponse])
def list_expiring_contracts(
    days: int = Query(90),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    contracts = contract_service.get_expiring_contracts(db, days_threshold=days)
    return restrict_to_vendor(db, current_user, contracts, "contracts")

@router.get("/expiring-certifications", response_model=List[CertificationResponse])
def list_expiring_certifications(
    days: int = Query(90),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    certs = contract_service.get_expiring_certifications(db, days_threshold=days)
    return restrict_to_vendor(db, current_user, certs, "certifications")

@router.get("/{contract_id}", response_model=ContractResponse)
def get_contract(
    contract_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    c = contract_service.get_contract_by_id(db, contract_id)
    if not c:
        raise HTTPException(status_code=404, detail="Contract not found")
    assert_owns(db, current_user, c.vendor_id, "contracts")
    return c

@router.get("/{contract_id}/document")
def download_contract_document(
    contract_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    import os

    c = contract_service.get_contract_by_id(db, contract_id)
    if not c:
        raise HTTPException(status_code=404, detail="Contract not found")
    assert_owns(db, current_user, c.vendor_id, "contracts")

    if not c.document_path:
        raise HTTPException(status_code=404, detail="No agreement document has been uploaded for this contract")
    if not os.path.exists(c.document_path):
        raise HTTPException(status_code=404, detail="The stored document is no longer available on the server")

    return FileResponse(path=c.document_path, filename=c.document_name or "contract.pdf")


def _pending_contract_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_contract_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_contract_rows_2(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_contract_totals_2(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_contract_rows_3(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_contract_totals_3(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_contract_rows_4(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_contract_totals_4(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_contract_rows_5(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_contract_totals_5(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_contract_rows_6(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_contract_totals_6(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals
