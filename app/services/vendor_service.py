from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
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

def get_all_vendors(db: Session):
    return db.query(Vendor).all()

def get_vendor(db: Session, vendor_id: int):
    return db.query(Vendor).filter(Vendor.id == vendor_id).first()

def update_vendor(db: Session, vendor_id: int, vendor: VendorUpdate):
    db_vendor = get_vendor(db, vendor_id)
    if not db_vendor:
        return None
    update_data = vendor.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_vendor, key, value)
    db.commit()
    db.refresh(db_vendor)
    return db_vendor
