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

def get_all_vendors(db: Session, skip: int = 0, limit: int = 100, category: Optional[str] = None, status: Optional[str] = None):
    query = db.query(Vendor)
    if category:
        query = query.filter(Vendor.category == category)
    if status:
        query = query.filter(Vendor.status == status)
    return query.offset(skip).limit(limit).all()

def get_vendor(db: Session, vendor_id: int):
    return db.query(Vendor).filter(Vendor.id == vendor_id).first()

def update_vendor(db: Session, vendor_id: int, vendor: VendorUpdate):
    db_vendor = get_vendor(db, vendor_id)
    if not db_vendor:
        return None
    for key, value in vendor.dict(exclude_unset=True).items():
        setattr(db_vendor, key, value)
    db.commit()
    db.refresh(db_vendor)
    return db_vendor

def delete_vendor(db: Session, vendor_id: int):
    db_vendor = get_vendor(db, vendor_id)
    if not db_vendor:
        return None
    db.delete(db_vendor)
    db.commit()
    return db_vendor
