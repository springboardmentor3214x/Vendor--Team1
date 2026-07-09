from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import get_db
from app.schemas.vendor import VendorCreate, VendorUpdate, VendorResponse
from app.services import vendor_service

router = APIRouter(prefix="/vendors", tags=["Vendors"])

@router.post("/", response_model=VendorResponse)
def add_vendor(vendor: VendorCreate, db: Session = Depends(get_db)):
    new_vendor = vendor_service.create_vendor(db, vendor)
    if not new_vendor:
        raise HTTPException(status_code=400, detail="Vendor with this email already exists")
    return new_vendor

@router.get("/", response_model=List[VendorResponse])
def view_vendors(db: Session = Depends(get_db)):
    return vendor_service.get_all_vendors(db)

@router.get("/{vendor_id}", response_model=VendorResponse)
def view_vendor(vendor_id: int, db: Session = Depends(get_db)):
    db_vendor = vendor_service.get_vendor(db, vendor_id)
    if not db_vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return db_vendor

@router.put("/{vendor_id}", response_model=VendorResponse)
def modify_vendor(vendor_id: int, vendor: VendorUpdate, db: Session = Depends(get_db)):
    updated = vendor_service.update_vendor(db, vendor_id, vendor)
    if not updated:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return updated
