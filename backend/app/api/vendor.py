from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.vendor import VendorCreate
from app.services.vendor_service import (
    create_vendor,
    get_all_vendors,
    get_vendor,
    update_vendor,
    delete_vendor
)

router = APIRouter()


@router.post("/vendors")
def add_vendor(vendor: VendorCreate, db: Session = Depends(get_db)):
    return create_vendor(db, vendor)


@router.get("/vendors")
def all_vendors(db: Session = Depends(get_db)):
    return get_all_vendors(db)


@router.get("/vendors/{vendor_id}")
def one_vendor(vendor_id: int, db: Session = Depends(get_db)):

    vendor = get_vendor(db, vendor_id)

    if vendor is None:
        raise HTTPException(status_code=404, detail="Vendor Not Found")

    return vendor


@router.put("/vendors/{vendor_id}")
def edit_vendor(vendor_id: int, vendor: VendorCreate, db: Session = Depends(get_db)):

    updated = update_vendor(db, vendor_id, vendor)

    if updated is None:
        raise HTTPException(status_code=404, detail="Vendor Not Found")

    return updated


@router.delete("/vendors/{vendor_id}")
def remove_vendor(vendor_id: int, db: Session = Depends(get_db)):

    deleted = delete_vendor(db, vendor_id)

    if deleted is None:
        raise HTTPException(status_code=404, detail="Vendor Not Found")

    return {"message": "Vendor Deleted Successfully"}