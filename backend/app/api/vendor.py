from fastapi import APIRouter, Depends, HTTPException, Query, Form, File, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from app.database.connection import get_db
from app.schemas.vendor import VendorCreate, VendorUpdate, VendorResponse, VendorDocumentResponse
from app.services import vendor_service
from app.services import notification_service
from app.core.dependencies import get_current_user, role_required
from app.core.roles import Roles, INTERNAL_ROLES
from app.models.user import User
from app.utils.uploads import (
    validate_upload,
    ALLOWED_DOCUMENT_EXTENSIONS,
    MAX_DOCUMENT_SIZE_BYTES,
)

router = APIRouter(prefix="/vendors", tags=["Vendors"])

@router.get("/stats")
def vendor_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(INTERNAL_ROLES))
):
    return vendor_service.get_vendor_stats(db)

@router.get("/recent", response_model=List[VendorResponse])
def recent_vendors(
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(INTERNAL_ROLES))
):
    return vendor_service.get_recent_vendors(db, limit)

@router.get("/me", response_model=VendorResponse)
def get_my_vendor_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from app.models.vendor import Vendor
    from sqlalchemy import func
    vendor = db.query(Vendor).filter(func.lower(Vendor.email) == current_user.email.lower()).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor profile not found for current user")
    return vendor

@router.get("/approved", response_model=List[VendorResponse])
def approved_vendors(
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(INTERNAL_ROLES))
):
    return vendor_service.get_assignable_vendors(db, category=category)

@router.post("/", response_model=VendorResponse, status_code=201)
def add_vendor(
    vendor: VendorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN, Roles.PROCUREMENT_MANAGER]))
):
    new_vendor = vendor_service.create_vendor(db, vendor, created_by=current_user.name)
    if not new_vendor:
        raise HTTPException(status_code=400, detail="Vendor with this email already exists")
    return new_vendor

@router.get("/", response_model=List[VendorResponse])
def view_vendors(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    category: Optional[str] = None,
    status: Optional[str] = None,
    approval_status: Optional[str] = None,
    keyword: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_dir: str = Query("asc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(INTERNAL_ROLES))
):
    return vendor_service.get_all_vendors(
        db, skip=skip, limit=limit, category=category, status=status,
        approval_status=approval_status, keyword=keyword,
        sort_by=sort_by, sort_dir=sort_dir
    )

@router.get("/{vendor_id}", response_model=VendorResponse)
def view_vendor(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    vendor = vendor_service.get_vendor(db, vendor_id)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    if current_user.role == Roles.VENDOR and vendor.email.lower() != current_user.email.lower():
        raise HTTPException(status_code=403, detail="You can only view your own vendor profile")
    return vendor

@router.put("/{vendor_id}", response_model=VendorResponse)
def modify_vendor(
    vendor_id: int, data: VendorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN, Roles.PROCUREMENT_MANAGER]))
):
    updated = vendor_service.update_vendor(db, vendor_id, data, updated_by=current_user.name)
    if not updated:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return updated

@router.delete("/{vendor_id}")
def remove_vendor(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN]))
):
    deleted = vendor_service.delete_vendor(db, vendor_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return {"message": "Vendor deleted successfully"}

@router.post("/{vendor_id}/approve")
def approve(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN, Roles.PROCUREMENT_MANAGER]))
):
    vendor = vendor_service.approve_vendor(db, vendor_id, current_user.name)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    notification_service.notify_vendor_approval_decision(db, vendor, approved=True)
    return {"message": "Vendor approved"}

@router.post("/{vendor_id}/reject")
def reject(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN, Roles.PROCUREMENT_MANAGER]))
):
    vendor = vendor_service.reject_vendor(db, vendor_id, current_user.name)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    notification_service.notify_vendor_approval_decision(db, vendor, approved=False)
    return {"message": "Vendor rejected"}


def _pending_vendor_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "title", "")),
            "state": getattr(item, "status", "Draft"),
            "owner": getattr(item, "created_by", None),
        })
    return rows


def _pending_vendor_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
        else:
            totals["other"] = totals.get("other", 0) + 1
    return totals


def _pending_vendor_rows_2(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "title", "")),
            "state": getattr(item, "status", "Draft"),
            "owner": getattr(item, "created_by", None),
        })
    return rows


def _pending_vendor_totals_2(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
        else:
            totals["other"] = totals.get("other", 0) + 1
    return totals


def _pending_vendor_rows_3(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "title", "")),
            "state": getattr(item, "status", "Draft"),
            "owner": getattr(item, "created_by", None),
        })
    return rows


def _pending_vendor_totals_3(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
        else:
            totals["other"] = totals.get("other", 0) + 1
    return totals


def _pending_vendor_rows_4(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "title", "")),
            "state": getattr(item, "status", "Draft"),
            "owner": getattr(item, "created_by", None),
        })
    return rows


def _pending_vendor_totals_4(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
        else:
            totals["other"] = totals.get("other", 0) + 1
    return totals


def _pending_vendor_rows_5(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "title", "")),
            "state": getattr(item, "status", "Draft"),
            "owner": getattr(item, "created_by", None),
        })
    return rows


def _pending_vendor_totals_5(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
        else:
            totals["other"] = totals.get("other", 0) + 1
    return totals
