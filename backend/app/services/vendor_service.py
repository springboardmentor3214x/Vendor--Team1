from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app.models.vendor import Vendor
from app.schemas.vendor import VendorCreate


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