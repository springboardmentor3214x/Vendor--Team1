from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app.models.vendor import Vendor
from app.schemas.vendor import VendorCreate
from sqlalchemy import or_
from sqlalchemy import func
from sqlalchemy import asc, desc


def create_vendor(db: Session, vendor: VendorCreate):

    new_vendor = Vendor(
    vendor_name=vendor.vendor_name,
    company_name=vendor.company_name,
    email=vendor.email,
    phone=vendor.phone,
    address=vendor.address,
    category=vendor.category,

    delivery_score=vendor.delivery_score,
    quality_score=vendor.quality_score,
    compliance_score=vendor.compliance_score,
    communication_score=vendor.communication_score,

    reliability_score=0,

    status=vendor.status
)

    try:
        db.add(new_vendor)
        db.commit()
        db.refresh(new_vendor)
        return new_vendor

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Vendor email already exists."
        )


def get_all_vendors(db: Session):
    return db.query(Vendor).all()


def get_vendor(db: Session, vendor_id: int):
    return db.query(Vendor).filter(Vendor.id == vendor_id).first()


def update_vendor(db: Session, vendor_id: int, vendor: VendorCreate):

    existing_vendor = db.query(Vendor).filter(
        Vendor.id == vendor_id
    ).first()

    if existing_vendor is None:
        return None

    existing_vendor.vendor_name = vendor.vendor_name
    existing_vendor.company_name = vendor.company_name
    existing_vendor.email = vendor.email
    existing_vendor.phone = vendor.phone
    existing_vendor.address = vendor.address
    existing_vendor.category = vendor.category

    existing_vendor.delivery_score = vendor.delivery_score
    existing_vendor.quality_score = vendor.quality_score
    existing_vendor.compliance_score = vendor.compliance_score
    existing_vendor.communication_score = vendor.communication_score

    existing_vendor.status = vendor.status

    db.commit()
    db.refresh(existing_vendor)

    return existing_vendor


def delete_vendor(db: Session, vendor_id: int):

    vendor = db.query(Vendor).filter(
        Vendor.id == vendor_id
    ).first()

    if vendor is None:
        return None

    db.delete(vendor)
    db.commit()

    return vendor
def approve_vendor(
    db: Session,
    vendor_id: int,
    approved_by: str
):

    vendor = db.query(Vendor).filter(
        Vendor.id == vendor_id
    ).first()

    if vendor is None:
        return None

    vendor.approval_status = "Approved"
    vendor.status = "Active"
    vendor.approved_by = approved_by

    db.commit()
    db.refresh(vendor)

    return vendor


def reject_vendor(
    db: Session,
    vendor_id: int,
    approved_by: str
):

    vendor = db.query(Vendor).filter(
        Vendor.id == vendor_id
    ).first()

    if vendor is None:
        return None

    vendor.approval_status = "Rejected"
    vendor.status = "Rejected"
    vendor.approved_by = approved_by

    db.commit()
    db.refresh(vendor)

    return vendor
def search_vendors(
    db: Session,
    keyword: str
):

    vendors = db.query(Vendor).filter(
        or_(
            Vendor.vendor_name.ilike(f"%{keyword}%"),
            Vendor.company_name.ilike(f"%{keyword}%"),
            Vendor.category.ilike(f"%{keyword}%")
        )
    ).all()

    return vendors
def filter_vendors_by_status(
    db: Session,
    status: str
):

    vendors = db.query(Vendor).filter(
        Vendor.status == status
    ).all()

    return vendors
def filter_vendors_by_category(
    db: Session,
    category: str
):

    vendors = db.query(Vendor).filter(
        Vendor.category == category
    ).all()

    return vendors
def vendor_dashboard(db: Session):

    total_vendors = db.query(Vendor).count()

    active_vendors = db.query(Vendor).filter(
        Vendor.status == "Active"
    ).count()

    pending_vendors = db.query(Vendor).filter(
        Vendor.status == "Pending"
    ).count()

    approved_vendors = db.query(Vendor).filter(
        Vendor.approval_status == "Approved"
    ).count()

    rejected_vendors = db.query(Vendor).filter(
        Vendor.approval_status == "Rejected"
    ).count()

    return {
        "total_vendors": total_vendors,
        "active_vendors": active_vendors,
        "pending_vendors": pending_vendors,
        "approved_vendors": approved_vendors,
        "rejected_vendors": rejected_vendors
    }
def get_vendors_paginated(
    db: Session,
    page: int = 1,
    limit: int = 10
):

    skip = (page - 1) * limit

    vendors = (
        db.query(Vendor)
        .offset(skip)
        .limit(limit)
        .all()
    )

    total = db.query(Vendor).count()

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "data": vendors
    }
def sort_vendors(
    db: Session,
    field: str,
    order: str
):

    allowed_fields = {
        "vendor_name": Vendor.vendor_name,
        "company_name": Vendor.company_name,
        "category": Vendor.category,
        "status": Vendor.status
    }

    if field not in allowed_fields:
        raise HTTPException(
            status_code=400,
            detail="Invalid sort field."
        )

    column = allowed_fields[field]

    if order.lower() == "desc":
        vendors = db.query(Vendor).order_by(desc(column)).all()
    else:
        vendors = db.query(Vendor).order_by(asc(column)).all()

    return vendors
def sort_vendors(
    db: Session,
    field: str,
    order: str
):

    allowed_fields = {
        "vendor_name": Vendor.vendor_name,
        "company_name": Vendor.company_name,
        "category": Vendor.category,
        "status": Vendor.status
    }

    if field not in allowed_fields:
        raise HTTPException(
            status_code=400,
            detail="Invalid sort field."
        )

    column = allowed_fields[field]

    if order.lower() == "desc":
        vendors = db.query(Vendor).order_by(desc(column)).all()
    else:
        vendors = db.query(Vendor).order_by(asc(column)).all()

    return vendors
def calculate_reliability_score(
    db: Session,
    vendor_id: int
):

    vendor = db.query(Vendor).filter(
        Vendor.id == vendor_id
    ).first()

    if vendor is None:
        return None

    vendor.reliability_score = (
        vendor.delivery_score +
        vendor.quality_score +
        vendor.compliance_score +
        vendor.communication_score
    )

    db.commit()
    db.refresh(vendor)

    return vendor
def top_vendors(
    db: Session,
    limit: int = 5
):

    vendors = (
        db.query(Vendor)
        .order_by(Vendor.reliability_score.desc())
        .limit(limit)
        .all()
    )

    return vendors
def bottom_vendors(
    db: Session,
    limit: int = 5
):

    vendors = (
        db.query(Vendor)
        .order_by(Vendor.reliability_score.asc())
        .limit(limit)
        .all()
    )

    return vendors
def vendor_performance_report(
    db: Session,
    vendor_id: int
):

    vendor = db.query(Vendor).filter(
        Vendor.id == vendor_id
    ).first()

    if vendor is None:
        return None

    score = vendor.reliability_score

    if score >= 90:
        performance = "Excellent"

    elif score >= 75:
        performance = "Good"

    elif score >= 60:
        performance = "Average"

    else:
        performance = "Poor"

    return {
        "vendor_id": vendor.id,
        "vendor_name": vendor.vendor_name,
        "company_name": vendor.company_name,
        "reliability_score": score,
        "performance": performance,
        "status": vendor.status,
        "approval_status": vendor.approval_status
    }
def update_vendor_scores(
    db: Session,
    vendor_id: int,
    scores
):

    vendor = db.query(Vendor).filter(
        Vendor.id == vendor_id
    ).first()

    if vendor is None:
        return None

    vendor.delivery_score = scores.delivery_score
    vendor.quality_score = scores.quality_score
    vendor.compliance_score = scores.compliance_score
    vendor.communication_score = scores.communication_score

    vendor.reliability_score = (
        vendor.delivery_score +
        vendor.quality_score +
        vendor.compliance_score +
        vendor.communication_score
    ) / 4

    db.commit()
    db.refresh(vendor)

    return vendor