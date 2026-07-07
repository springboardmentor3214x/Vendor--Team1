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