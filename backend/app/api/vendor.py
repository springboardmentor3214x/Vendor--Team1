from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.connection import get_db
from app.schemas.vendor import VendorCreate, VendorUpdate, VendorResponse
from app.services import vendor_service

router = APIRouter(prefix="/vendors", tags=["Vendors"])

@router.post("/", response_model=VendorResponse, status_code=201)
def add_vendor(vendor: VendorCreate, db: Session = Depends(get_db)):
    new_vendor = vendor_service.create_vendor(db, vendor)
    if not new_vendor:
        raise HTTPException(status_code=400, detail="Vendor with this email already exists")
    return new_vendor

@router.get("/", response_model=List[VendorResponse])
def view_vendors(skip: int = Query(0, ge=0), limit: int = Query(100, le=1000), category: Optional[str] = None, status: Optional[str] = None, db: Session = Depends(get_db)):
    return vendor_service.get_all_vendors(db, skip=skip, limit=limit, category=category, status=status)

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

@router.delete("/{vendor_id}")
def remove_vendor(vendor_id: int, db: Session = Depends(get_db)):
    deleted = vendor_service.delete_vendor(db, vendor_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return {"message": "Vendor deleted successfully"}
