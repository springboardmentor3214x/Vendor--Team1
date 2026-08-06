from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional

from app.models.vendor import Vendor
from app.schemas.vendor import VendorCreate, VendorUpdate


def create_vendor(db: Session, vendor: VendorCreate):
    db_vendor = Vendor(**vendor.dict())
    try:
        db.add(db_vendor)
        db.commit()
        db.refresh(db_vendor)
        return db_vendor
    except IntegrityError:
        db.rollback()
        return None


def get_all_vendors(db: Session, skip: int = 0, limit: int = 100,
                    category: Optional[str] = None, status: Optional[str] = None):
    query = db.query(Vendor)
    if category:
        query = query.filter(Vendor.category == category)
    if status:
        query = query.filter(Vendor.status == status)
    return query.offset(skip).limit(limit).all()


def get_vendor(db: Session, vendor_id: int):
    return db.query(Vendor).filter(Vendor.id == vendor_id).first()


def update_vendor(db: Session, vendor_id: int, data: VendorUpdate):
    vendor = get_vendor(db, vendor_id)
    if not vendor:
        return None
    for key, value in data.dict(exclude_unset=True).items():
        setattr(vendor, key, value)
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


def delete_vendor(db: Session, vendor_id: int):
    vendor = get_vendor(db, vendor_id)
    if not vendor:
        return None
    check_vendor_active_activities(db, vendor_id)
    db.delete(vendor)
    db.commit()
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
    sync_user_status_by_email(db, vendor.email, "Rejected")
    db.commit()
    db.refresh(vendor)
    return vendor


def block_vendor(db: Session, vendor_id: int):
    vendor = get_vendor(db, vendor_id)
    if not vendor:
        return None
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


HIGH_RISK_THRESHOLD = 60.0


def get_vendor_stats(db: Session) -> dict:
    all_vendors = db.query(Vendor).all()
    total = len(all_vendors)
    approved = sum(1 for v in all_vendors if v.approval_status == "Approved")
    pending = sum(1 for v in all_vendors if v.approval_status == "Pending")
    suspended = sum(1 for v in all_vendors if v.status == "Inactive")
    rejected = sum(1 for v in all_vendors if v.approval_status == "Rejected")
    high_risk = sum(
        1 for v in all_vendors
        if v.approval_status == "Approved" and v.reliability_score < HIGH_RISK_THRESHOLD
    )
    return {
        "total": total,
        "approved": approved,
        "pending_review": pending,
        "suspended": suspended,
        "rejected": rejected,
        "high_risk": high_risk,
    }


def get_recent_vendors(db: Session, limit: int = 5):
    return db.query(Vendor).order_by(Vendor.id.desc()).limit(limit).all()
