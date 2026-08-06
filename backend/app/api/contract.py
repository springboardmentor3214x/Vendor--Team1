from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.database.connection import get_db
from app.schemas.contract import ContractCreate, ContractUpdate, ContractResponse
from app.schemas.certification import CertificationCreate, CertificationResponse
from app.schemas.compliance_record import ComplianceRecordCreate, ComplianceRecordResponse
from app.services import contract_service
from app.core.dependencies import get_current_user, role_required
from app.core.roles import Roles
from app.models.user import User

router = APIRouter(prefix="/contracts", tags=["Contracts & Compliance"])


# Contract Repository APIs
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
    return contract_service.get_all_contracts(db)


@router.get("/expiring", response_model=List[ContractResponse])
def list_expiring_contracts(
    days: int = Query(90),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return contract_service.get_expiring_contracts(db, days_threshold=days)


@router.get("/{contract_id}", response_model=ContractResponse)
def get_contract(
    contract_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    c = contract_service.get_contract_by_id(db, contract_id)
    if not c:
        raise HTTPException(status_code=404, detail="Contract not found")
    return c


@router.put("/{contract_id}", response_model=ContractResponse)
def update_contract(
    contract_id: int,
    data: ContractUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN, Roles.PROCUREMENT_MANAGER]))
):
    return contract_service.update_contract(db, contract_id, data)


@router.post("/{contract_id}/renew", response_model=ContractResponse)
def renew_contract(
    contract_id: int,
    new_end_date: date,
    new_value: Optional[float] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN, Roles.PROCUREMENT_MANAGER]))
):
    return contract_service.renew_contract(db, contract_id, new_end_date, new_value)


@router.delete("/{contract_id}")
def delete_contract(
    contract_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN]))
):
    return contract_service.delete_contract(db, contract_id)


# Certifications APIs
@router.post("/certifications", response_model=CertificationResponse, status_code=201)
def add_certification(
    data: CertificationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN, Roles.PROCUREMENT_MANAGER, Roles.VENDOR]))
):
    return contract_service.add_certification(db, data)


@router.get("/certifications/{vendor_id}", response_model=List[CertificationResponse])
def get_certifications(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return contract_service.get_vendor_certifications(db, vendor_id)


@router.delete("/certifications/{cert_id}")
def delete_certification(
    cert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN, Roles.PROCUREMENT_MANAGER]))
):
    return contract_service.delete_certification(db, cert_id)


# Compliance APIs
@router.post("/compliance", response_model=ComplianceRecordResponse, status_code=201)
def record_compliance(
    data: ComplianceRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN, Roles.PROCUREMENT_MANAGER, Roles.AUDITOR]))
):
    return contract_service.record_compliance(db, data)


@router.get("/compliance/dashboard")
def get_compliance_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return contract_service.get_compliance_dashboard(db)


@router.get("/compliance/{vendor_id}", response_model=List[ComplianceRecordResponse])
def get_vendor_compliance(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return contract_service.get_vendor_compliance(db, vendor_id)


@router.put("/compliance/{id}", response_model=ComplianceRecordResponse)
def update_compliance_status(
    id: int,
    status: str,
    remarks: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN, Roles.PROCUREMENT_MANAGER, Roles.AUDITOR]))
):
    return contract_service.update_compliance_status(db, id, status, current_user.name, remarks)
