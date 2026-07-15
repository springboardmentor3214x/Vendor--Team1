from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import get_db
from app.schemas.procurement import ProcurementCreate, ProcurementResponse
from app.services import procurement_service

router = APIRouter(prefix="/procurements", tags=["Procurements"])

@router.post("/", response_model=ProcurementResponse, status_code=201)
def add_procurement(procurement: ProcurementCreate, db: Session = Depends(get_db)):
    return procurement_service.create_procurement(db, procurement)

@router.get("/", response_model=List[ProcurementResponse])
def view_procurements(db: Session = Depends(get_db)):
    return procurement_service.get_all_procurements(db)

@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):
    return procurement_service.procurement_dashboard(db)

@router.get("/search")
def search(keyword: str, db: Session = Depends(get_db)):
    return procurement_service.search_procurements(db, keyword)

@router.get("/filter", response_model=List[ProcurementResponse])
def filter_by_status(status: str, db: Session = Depends(get_db)):
    return procurement_service.filter_procurements(db, status)

@router.get("/vendor/{vendor_id}", response_model=List[ProcurementResponse])
def view_by_vendor(vendor_id: int, db: Session = Depends(get_db)):
    return procurement_service.get_procurements_by_vendor(db, vendor_id)

@router.get("/{procurement_id}", response_model=ProcurementResponse)
def view_procurement(procurement_id: int, db: Session = Depends(get_db)):
    proc = procurement_service.get_procurement(db, procurement_id)
    if not proc:
        raise HTTPException(status_code=404, detail="Procurement not found")
    return proc

@router.put("/{procurement_id}", response_model=ProcurementResponse)
def edit_procurement(procurement_id: int, procurement: ProcurementCreate, db: Session = Depends(get_db)):
    updated = procurement_service.update_procurement(db, procurement_id, procurement)
    if not updated:
        raise HTTPException(status_code=404, detail="Procurement not found")
    return updated

@router.delete("/{procurement_id}")
def remove_procurement(procurement_id: int, db: Session = Depends(get_db)):
    deleted = procurement_service.delete_procurement(db, procurement_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Procurement not found")
    return {"message": "Procurement deleted successfully"}

@router.post("/{procurement_id}/approve")
def approve(procurement_id: int, db: Session = Depends(get_db)):
    proc = procurement_service.approve_procurement(db, procurement_id, "Manager")
    if not proc:
        raise HTTPException(status_code=404, detail="Procurement not found")
    return {"message": "Procurement approved"}

@router.post("/{procurement_id}/reject")
def reject(procurement_id: int, db: Session = Depends(get_db)):
    proc = procurement_service.reject_procurement(db, procurement_id, "Manager")
    if not proc:
        raise HTTPException(status_code=404, detail="Procurement not found")
    return {"message": "Procurement rejected"}

@router.post("/{procurement_id}/deliver")
def deliver(procurement_id: int, db: Session = Depends(get_db)):
    proc = procurement_service.mark_delivered(db, procurement_id)
    if not proc:
        raise HTTPException(status_code=404, detail="Procurement not found")
    return {"message": "Marked as delivered"}

@router.post("/{procurement_id}/complete")
def complete(procurement_id: int, db: Session = Depends(get_db)):
    proc = procurement_service.mark_completed(db, procurement_id)
    if not proc:
        raise HTTPException(status_code=404, detail="Procurement not found")
    return {"message": "Marked as completed"}
