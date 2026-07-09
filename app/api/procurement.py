from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import get_db
from app.schemas.procurement import ProcurementCreate, ProcurementResponse
from app.services import procurement_service

router = APIRouter(prefix="/procurements", tags=["Procurements"])

@router.post("/", response_model=ProcurementResponse, status_code=201)
def add_procurement(procurement: ProcurementCreate, db: Session = Depends(get_db)):
    """Create a new procurement request."""
    return procurement_service.create_procurement(db, procurement)

@router.get("/", response_model=List[ProcurementResponse])
def view_procurements(db: Session = Depends(get_db)):
    """List all procurements."""
    return procurement_service.get_all_procurements(db)

@router.get("/{procurement_id}", response_model=ProcurementResponse)
def view_procurement(procurement_id: int, db: Session = Depends(get_db)):
    """Get procurement by ID."""
    proc = procurement_service.get_procurement(db, procurement_id)
    if not proc:
        raise HTTPException(status_code=404, detail="Procurement not found")
    return proc

@router.put("/{procurement_id}", response_model=ProcurementResponse)
def edit_procurement(procurement_id: int, procurement: ProcurementCreate, db: Session = Depends(get_db)):
    """Update a procurement."""
    updated = procurement_service.update_procurement(db, procurement_id, procurement)
    if not updated:
        raise HTTPException(status_code=404, detail="Procurement not found")
    return updated

@router.delete("/{procurement_id}")
def remove_procurement(procurement_id: int, db: Session = Depends(get_db)):
    """Delete a procurement."""
    deleted = procurement_service.delete_procurement(db, procurement_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Procurement not found")
    return {"message": "Procurement deleted successfully"}
