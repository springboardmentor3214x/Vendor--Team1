from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.vendor import Vendor
from app.schemas.vendor import VendorCreate

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
