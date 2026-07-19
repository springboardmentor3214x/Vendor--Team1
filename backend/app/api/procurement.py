from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.connection import get_db
from app.schemas.procurement import ProcurementCreate, ProcurementResponse, StatusHistoryResponse
from app.services import procurement_service, notification_service
from app.core.dependencies import get_current_user, role_required
from app.core.roles import Roles
from app.models.user import User

router = APIRouter(prefix="/procurements", tags=["Procurements"])

class AssignVendorRequest(BaseModel):
    vendor_id: int
    acknowledge_risk: bool = False

class ApprovalActionRequest(BaseModel):
    remarks: Optional[str] = None

@router.post("/", response_model=ProcurementResponse, status_code=201)
def add_procurement(
    data: ProcurementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN, Roles.PROCUREMENT_MANAGER, Roles.SUPPLY_CHAIN_MANAGER]))
):
    if not data.requested_by:
        data.requested_by = current_user.name
    proc = procurement_service.create_procurement(db, data)
    if proc.status != "Draft":
        notification_service.notify_procurement_submitted(db, proc)
    return proc

@router.get("/", response_model=List[ProcurementResponse])
def view_procurements(
    department: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    keyword: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == Roles.VENDOR:
        from app.models.vendor import Vendor
        from sqlalchemy import func
        vendor = db.query(Vendor).filter(func.lower(Vendor.email) == current_user.email.lower()).first()
        if vendor:
            return procurement_service.get_procurements_by_vendor(db, vendor.id)
        return []
    return procurement_service.get_all_procurements(db, department=department, status=status, priority=priority, keyword=keyword)

@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([
        Roles.ADMIN, Roles.PROCUREMENT_MANAGER, Roles.SUPPLY_CHAIN_MANAGER,
        Roles.FINANCE_OFFICER, Roles.AUDITOR,
    ]))
):
    return procurement_service.procurement_dashboard(db)

def current_vendor_id(db: Session, current_user: User) -> Optional[int]:
    if current_user.role != Roles.VENDOR:
        return None
    from app.models.vendor import Vendor
    from sqlalchemy import func
    vendor = db.query(Vendor).filter(func.lower(Vendor.email) == current_user.email.lower()).first()
    return vendor.id if vendor else -1

def assert_vendor_may_read(db: Session, current_user: User, proc):
    vendor_id = current_vendor_id(db, current_user)
    if vendor_id is not None and proc.vendor_id != vendor_id:
        raise HTTPException(
            status_code=403,
            detail="You can only view procurement requests assigned to you"
        )

@router.get("/search")
def search(
    keyword: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    results = procurement_service.search_procurements(db, keyword)
    vendor_id = current_vendor_id(db, current_user)
    if vendor_id is not None:
        results = [p for p in results if p.vendor_id == vendor_id]
    return results

@router.get("/filter", response_model=List[ProcurementResponse])
def filter_by_status(
    status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    results = procurement_service.filter_procurements(db, status)
    vendor_id = current_vendor_id(db, current_user)
    if vendor_id is not None:
        results = [p for p in results if p.vendor_id == vendor_id]
    return results

@router.get("/vendor/{vendor_id}", response_model=List[ProcurementResponse])
def by_vendor(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    own_vendor_id = current_vendor_id(db, current_user)
    if own_vendor_id is not None and own_vendor_id != vendor_id:
        raise HTTPException(status_code=403, detail="You can only view your own procurement records")
    return procurement_service.get_procurements_by_vendor(db, vendor_id)

@router.get("/{procurement_id}", response_model=ProcurementResponse)
def view_procurement(
    procurement_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    proc = procurement_service.get_procurement(db, procurement_id)
    if not proc:
        raise HTTPException(status_code=404, detail="Procurement not found")
    assert_vendor_may_read(db, current_user, proc)
    return proc

@router.get("/{procurement_id}/history", response_model=List[StatusHistoryResponse])
def get_history(
    procurement_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    proc = procurement_service.get_procurement(db, procurement_id)
    if not proc:
        raise HTTPException(status_code=404, detail="Procurement not found")
    assert_vendor_may_read(db, current_user, proc)
    return procurement_service.get_status_history(db, procurement_id)

@router.put("/{procurement_id}", response_model=ProcurementResponse)
def edit_procurement(
    procurement_id: int,
    data: ProcurementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN, Roles.PROCUREMENT_MANAGER, Roles.SUPPLY_CHAIN_MANAGER]))
):
    updated = procurement_service.update_procurement(db, procurement_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Procurement not found")
    return updated

@router.delete("/{procurement_id}")
def remove_procurement(
    procurement_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN, Roles.PROCUREMENT_MANAGER]))
):
    deleted = procurement_service.delete_procurement(db, procurement_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Procurement not found")
    return {"message": "Procurement deleted successfully"}

@router.post("/{procurement_id}/approve")
def approve(
    procurement_id: int,
    body: Optional[ApprovalActionRequest] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN, Roles.PROCUREMENT_MANAGER]))
):
    remarks = body.remarks if body else "Approved"
    proc = procurement_service.approve_procurement(db, procurement_id, current_user.name, remarks=remarks)
    if not proc:
        raise HTTPException(status_code=404, detail="Procurement not found")
    return {"message": "Procurement approved", "procurement": proc}


def _pending_procurement_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "label", "")),
            "state": getattr(item, "status", "Unverified"),
            "updated": getattr(item, "updated_at", None),
        })
    return rows


def _pending_procurement_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_procurement_rows_2(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "label", "")),
            "state": getattr(item, "status", "Unverified"),
            "updated": getattr(item, "updated_at", None),
        })
    return rows


def _pending_procurement_totals_2(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_procurement_rows_3(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "label", "")),
            "state": getattr(item, "status", "Unverified"),
            "updated": getattr(item, "updated_at", None),
        })
    return rows


def _pending_procurement_totals_3(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_procurement_rows_4(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "label", "")),
            "state": getattr(item, "status", "Unverified"),
            "updated": getattr(item, "updated_at", None),
        })
    return rows


def _pending_procurement_totals_4(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_procurement_rows_5(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "label", "")),
            "state": getattr(item, "status", "Unverified"),
            "updated": getattr(item, "updated_at", None),
        })
    return rows


def _pending_procurement_totals_5(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_procurement_rows_6(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "label", "")),
            "state": getattr(item, "status", "Unverified"),
            "updated": getattr(item, "updated_at", None),
        })
    return rows
