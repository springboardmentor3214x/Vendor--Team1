from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, or_
from fastapi import HTTPException
from datetime import datetime
from typing import Optional
from app.models.vendor import Vendor
from app.schemas.vendor import VendorCreate, VendorUpdate
from app.core.risk import calculate_risk_level, is_high_risk, vendor_has_performance_data
from app.core.vendor_categories import VENDOR_CATEGORIES, ALL_VENDOR_CATEGORIES

UNIQUE_VENDOR_FIELDS = [
    ("email", "A vendor with this email address already exists"),
    ("gst_number", "A vendor with this GST number already exists"),
    ("pan_number", "A vendor with this PAN number already exists"),
    ("company_registration_number", "A vendor with this company registration number already exists"),
]

def validate_vendor_uniqueness(db: Session, data: dict, exclude_vendor_id: Optional[int] = None):
    for field, message in UNIQUE_VENDOR_FIELDS:
        value = data.get(field)
        if not value:
            continue
        column = getattr(Vendor, field)
        query = db.query(Vendor).filter(func.lower(column) == str(value).strip().lower())
        if exclude_vendor_id is not None:
            query = query.filter(Vendor.id != exclude_vendor_id)
        if query.first():
            raise HTTPException(status_code=400, detail=message)

def create_vendor(db: Session, vendor: VendorCreate, created_by: Optional[str] = None):
    data = vendor.model_dump()
    validate_vendor_uniqueness(db, data)

    data.setdefault("delivery_score", 0.0)
    data.setdefault("quality_score", 0.0)
    data.setdefault("communication_score", 0.0)
    data.setdefault("service_score", 0.0)
    data.setdefault("reliability_score", 0.0)

    now = datetime.utcnow()
    data["created_by"] = created_by
    data["created_at"] = now
    data["updated_by"] = created_by
    data["updated_at"] = now

    db_vendor = Vendor(**data)
    try:
        db.add(db_vendor)
        db.commit()
        db.refresh(db_vendor)
        return db_vendor
    except IntegrityError:
        db.rollback()
        return None

def get_all_vendors(db: Session, skip: int = 0, limit: int = 100,
                    category: Optional[str] = None, status: Optional[str] = None,
                    approval_status: Optional[str] = None, keyword: Optional[str] = None,
                    sort_by: Optional[str] = None, sort_dir: str = "asc"):
    query = db.query(Vendor)
    if category and category != "All":
        query = query.filter(Vendor.category == category)
    if status and status != "All":
        query = query.filter(Vendor.status == status)
    if approval_status and approval_status != "All":
        query = query.filter(Vendor.approval_status == approval_status)
    if keyword:
        pattern = f"%{keyword.strip()}%"
        conditions = [
            Vendor.vendor_name.ilike(pattern),
            Vendor.company_name.ilike(pattern),
            Vendor.contact_person.ilike(pattern),
            Vendor.email.ilike(pattern),
            Vendor.gst_number.ilike(pattern),
        ]
        digits = "".join(ch for ch in keyword if ch.isdigit())
        if digits:
            conditions.append(Vendor.id == int(digits))
        query = query.filter(or_(*conditions))

    sortable = {
        "id": Vendor.id,
        "vendor_name": Vendor.vendor_name,
        "company_name": Vendor.company_name,
        "category": Vendor.category,
        "email": Vendor.email,
        "status": Vendor.status,
        "approval_status": Vendor.approval_status,
        "reliability_score": Vendor.reliability_score,
        "created_at": Vendor.created_at,
    }
    column = sortable.get(sort_by or "id", Vendor.id)
    query = query.order_by(column.desc() if sort_dir == "desc" else column.asc())

    return query.offset(skip).limit(limit).all()

def get_assignable_vendors(db: Session, category: Optional[str] = None):
    query = db.query(Vendor).filter(
        Vendor.approval_status == "Approved",
        Vendor.status == "Active"
    )
    if category and category != "All":
        query = query.filter(Vendor.category == category)
    return query.order_by(Vendor.reliability_score.desc()).all()

def get_vendor(db: Session, vendor_id: int):
    return db.query(Vendor).filter(Vendor.id == vendor_id).first()

def update_vendor(db: Session, vendor_id: int, data: VendorUpdate, updated_by: Optional[str] = None):
    vendor = get_vendor(db, vendor_id)
    if not vendor:
        return None
    payload = data.model_dump(exclude_unset=True)

    new_category = payload.get("category")
    if new_category is not None and new_category not in ALL_VENDOR_CATEGORIES:
        if new_category != vendor.category:
            allowed = ", ".join(VENDOR_CATEGORIES)
            raise HTTPException(
                status_code=400,
                detail=f"Invalid vendor category '{new_category}'. Allowed categories: {allowed}"
            )

    validate_vendor_uniqueness(db, payload, exclude_vendor_id=vendor_id)
    for key, value in payload.items():
        setattr(vendor, key, value)
    vendor.updated_by = updated_by
    vendor.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(vendor)
    return vendor


def _pending_vendor_service_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_vendor_service_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_vendor_service_rows_2(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_vendor_service_totals_2(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_vendor_service_rows_3(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_vendor_service_totals_3(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_vendor_service_rows_4(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_vendor_service_totals_4(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_vendor_service_rows_5(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_vendor_service_totals_5(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_vendor_service_rows_6(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_vendor_service_totals_6(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals
