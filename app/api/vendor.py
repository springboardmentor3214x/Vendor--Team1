from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import get_db
from app.schemas.vendor import VendorCreate, VendorResponse
from app.services.vendor_service import create_vendor, get_all_vendors

router = APIRouter(prefix="/vendors", tags=["Vendors"])

@router.post("/", response_model=VendorResponse)
def add_vendor(vendor: VendorCreate, db: Session = Depends(get_db)):
    new_vendor = create_vendor(db, vendor)
    if not new_vendor:
        raise HTTPException(status_code=400, detail="Vendor with this email already exists")
    return new_vendor

@router.get("/", response_model=List[VendorResponse])
def view_vendors(db: Session = Depends(get_db)):
    return get_all_vendors(db)
