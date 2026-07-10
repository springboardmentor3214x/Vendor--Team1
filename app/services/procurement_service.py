from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_, func
from fastapi import HTTPException
from datetime import datetime
from app.models.procurement import Procurement
from app.schemas.procurement import ProcurementCreate

def create_procurement(db: Session, procurement: ProcurementCreate):
    total_price = procurement.quantity * procurement.unit_price
    new_proc = Procurement(
        item_name=procurement.item_name, vendor_id=procurement.vendor_id,
        quantity=procurement.quantity, unit_price=procurement.unit_price,
        total_price=total_price, expected_delivery_date=procurement.expected_delivery_date,
        status="Pending"
    )
    try:
        db.add(new_proc)
        db.commit()
        db.refresh(new_proc)
        return new_proc
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

def get_all_procurements(db: Session):
    return db.query(Procurement).all()

def get_procurement(db: Session, procurement_id: int):
    return db.query(Procurement).filter(Procurement.id == procurement_id).first()

def update_procurement(db: Session, procurement_id: int, data: ProcurementCreate):
    existing = get_procurement(db, procurement_id)
    if not existing:
        return None
    existing.item_name = data.item_name
    existing.vendor_id = data.vendor_id
    existing.quantity = data.quantity
    existing.unit_price = data.unit_price
    existing.total_price = data.quantity * data.unit_price
    existing.expected_delivery_date = data.expected_delivery_date
    db.commit()
    db.refresh(existing)
    return existing

def delete_procurement(db: Session, procurement_id: int):
    proc = get_procurement(db, procurement_id)
    if not proc:
        return None
    db.delete(proc)
    db.commit()
    return proc

def approve_procurement(db: Session, procurement_id: int, approved_by: str):
    proc = get_procurement(db, procurement_id)
    if not proc:
        return None
    proc.approval_status = "Approved"
    proc.status = "Approved"
    proc.approved_by = approved_by
    db.commit()
    db.refresh(proc)
    return proc

def reject_procurement(db: Session, procurement_id: int, approved_by: str):
    proc = get_procurement(db, procurement_id)
    if not proc:
        return None
    proc.approval_status = "Rejected"
    proc.status = "Rejected"
    proc.approved_by = approved_by
    db.commit()
    db.refresh(proc)
    return proc

def filter_procurements(db: Session, status: str):
    return db.query(Procurement).filter(Procurement.status == status).all()

def search_procurements(db: Session, keyword: str):
    return db.query(Procurement).filter(or_(Procurement.item_name.ilike(f"%{keyword}%"))).all()
