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


def check_vendor_active_activities(db: Session, vendor_id: int):
    from app.models.procurement import Procurement
    from app.models.purchase_order import PurchaseOrder
    from app.models.contract import Contract
    from fastapi import HTTPException

    active_po = db.query(PurchaseOrder).filter(
        PurchaseOrder.vendor_id == vendor_id,
        PurchaseOrder.status.in_(["Issued", "In Transit", "Pending"])
    ).first()
    if active_po:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete or deactivate vendor with active Purchase Order #{active_po.po_number}. Complete or cancel orders first."
        )

    active_proc = db.query(Procurement).filter(
        Procurement.vendor_id == vendor_id,
        Procurement.status.in_(["Approved", "In Progress", "Pending"])
    ).first()
    if active_proc:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete or deactivate vendor with active Procurement Request #{active_proc.request_number or active_proc.id}."
        )

    active_contract = db.query(Contract).filter(
        Contract.vendor_id == vendor_id,
        Contract.status == "Active"
    ).first()
    if active_contract:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete or deactivate vendor with active Contract #{active_contract.contract_number or active_contract.id}."
        )


def check_vendor_has_history(db: Session, vendor_id: int):
    from app.models.procurement import Procurement
    from app.models.purchase_order import PurchaseOrder
    from app.models.contract import Contract

    referencing = [
        ("procurement request", db.query(Procurement).filter(Procurement.vendor_id == vendor_id).count()),
        ("purchase order", db.query(PurchaseOrder).filter(PurchaseOrder.vendor_id == vendor_id).count()),
        ("contract", db.query(Contract).filter(Contract.vendor_id == vendor_id).count()),
    ]
    blocking = [(label, count) for label, count in referencing if count]

    if blocking:
        summary = ", ".join(f"{count} {label}{'s' if count > 1 else ''}" for label, count in blocking)
        raise HTTPException(
            status_code=400,
            detail=(
                f"This vendor cannot be deleted because it is referenced by {summary}. "
                f"Deactivate the vendor instead to keep the procurement history intact."
            )
        )


def delete_vendor(db: Session, vendor_id: int):
    vendor = get_vendor(db, vendor_id)
    if not vendor:
        return None
    check_vendor_active_activities(db, vendor_id)
    check_vendor_has_history(db, vendor_id)

    try:
        db.delete(vendor)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=(
                "This vendor cannot be deleted because other records still reference it. "
                "Deactivate the vendor instead to keep its history intact."
            )
        )
    return vendor


def sync_user_status_by_email(db: Session, email: str, status: str):
    from app.models.user import User
    user = db.query(User).filter(User.email == email).first()
    if user:
        user.account_status = status


def approve_vendor(db: Session, vendor_id: int, approved_by: str):
    vendor = get_vendor(db, vendor_id)
    if not vendor:
        return None
    vendor.approval_status = "Approved"
    vendor.status = "Active"
    vendor.approved_by = approved_by
    vendor.approved_at = datetime.utcnow()
    vendor.updated_by = approved_by
    vendor.updated_at = datetime.utcnow()
    sync_user_status_by_email(db, vendor.email, "Active")
    db.commit()
    db.refresh(vendor)
    return vendor


def reject_vendor(db: Session, vendor_id: int, approved_by: str):
    vendor = get_vendor(db, vendor_id)
    if not vendor:
        return None
    check_vendor_active_activities(db, vendor_id)
    vendor.approval_status = "Rejected"
    vendor.status = "Rejected"
    vendor.approved_by = approved_by
    vendor.approved_at = datetime.utcnow()
    vendor.updated_by = approved_by
    vendor.updated_at = datetime.utcnow()
    sync_user_status_by_email(db, vendor.email, "Rejected")
    db.commit()
    db.refresh(vendor)
    return vendor


def block_vendor(db: Session, vendor_id: int):
    vendor = get_vendor(db, vendor_id)
    if not vendor:
        return None
    check_vendor_active_activities(db, vendor_id)
    vendor.status = "Blocked"
    sync_user_status_by_email(db, vendor.email, "Blocked")
    db.commit()
    db.refresh(vendor)
    return vendor


def deactivate_vendor(db: Session, vendor_id: int):
    vendor = get_vendor(db, vendor_id)
    if not vendor:
        return None
    check_vendor_active_activities(db, vendor_id)
    vendor.status = "Inactive"
    sync_user_status_by_email(db, vendor.email, "Deactivated")
    db.commit()
    db.refresh(vendor)
    return vendor


def activate_vendor(db: Session, vendor_id: int):
    vendor = get_vendor(db, vendor_id)
    if not vendor:
        return None
    if vendor.approval_status != "Approved":
        return None
    vendor.status = "Active"
    sync_user_status_by_email(db, vendor.email, "Active")
    db.commit()
    db.refresh(vendor)
    return vendor


def suspend_vendor(db: Session, vendor_id: int):
    return deactivate_vendor(db, vendor_id)


def update_vendor_scores(db: Session, vendor_id: int):
    from app.services.performance_service import calculate_vendor_metrics

    vendor = get_vendor(db, vendor_id)
    if not vendor:
        return None

    metrics = calculate_vendor_metrics(db, vendor_id)

    vendor.delivery_score = metrics["delivery_score"]
    vendor.quality_score = metrics["quality_score"]
    vendor.communication_score = metrics["communication_score"]
    vendor.service_score = metrics["service_score"]
    vendor.reliability_score = metrics["overall_performance_score"]

    db.commit()
    db.refresh(vendor)
    return vendor


def get_vendor_stats(db: Session) -> dict:
    all_vendors = db.query(Vendor).all()
    total = len(all_vendors)
    approved = sum(1 for v in all_vendors if v.approval_status == "Approved")
    pending = sum(1 for v in all_vendors if v.approval_status == "Pending")
    active = sum(1 for v in all_vendors if v.status == "Active")
    inactive = sum(1 for v in all_vendors if v.status == "Inactive")
    suspended = sum(1 for v in all_vendors if v.status in ("Inactive", "Suspended", "Blocked"))
    rejected = sum(1 for v in all_vendors if v.approval_status == "Rejected")
    high_risk = sum(
        1 for v in all_vendors
        if v.approval_status == "Approved"
        and is_high_risk(v.reliability_score, vendor_has_performance_data(db, v.id))
    )
    return {
        "total": total,
        "approved": approved,
        "pending_review": pending,
        "active": active,
        "inactive": inactive,
        "suspended": suspended,
        "rejected": rejected,
        "high_risk": high_risk,
    }


def get_recent_vendors(db: Session, limit: int = 5):
    return db.query(Vendor).order_by(Vendor.id.desc()).limit(limit).all()
