from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app.models.vendor import Vendor
from app.schemas.vendor import VendorCreate
from sqlalchemy import or_
from sqlalchemy import func


def create_vendor(db: Session, vendor: VendorCreate):

    new_vendor = Vendor(
        vendor_name=vendor.vendor_name,
        company_name=vendor.company_name,
        email=vendor.email,
        phone=vendor.phone,
        address=vendor.address,
        category=vendor.category,
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