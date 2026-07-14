from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.models.procurement import Procurement
from app.schemas.procurement import ProcurementCreate

def create_procurement(db: Session, procurement: ProcurementCreate):
    total_price = procurement.quantity * procurement.unit_price
    new_procurement = Procurement(
        item_name=procurement.item_name,
        vendor_id=procurement.vendor_id,
        quantity=procurement.quantity,
        unit_price=procurement.unit_price,
        total_price=total_price,
        expected_delivery_date=procurement.expected_delivery_date,
        status="Pending"
    )
    try:
        db.add(new_procurement)
        db.commit()
        db.refresh(new_procurement)
        return new_procurement
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

def get_all_procurements(db: Session):
    return db.query(Procurement).all()

def get_procurement(db: Session, procurement_id: int):
    return db.query(Procurement).filter(Procurement.id == procurement_id).first()

def update_procurement(db: Session, procurement_id: int, procurement: ProcurementCreate):
    existing = get_procurement(db, procurement_id)
    if not existing:
        return None
    existing.item_name = procurement.item_name
    existing.vendor_id = procurement.vendor_id
    existing.quantity = procurement.quantity
    existing.unit_price = procurement.unit_price
    existing.total_price = procurement.quantity * procurement.unit_price
    existing.expected_delivery_date = procurement.expected_delivery_date
    db.commit()
    db.refresh(existing)
    return existing

def delete_procurement(db: Session, procurement_id: int):
    procurement = get_procurement(db, procurement_id)
    if not procurement:
        return None
    db.delete(procurement)
    db.commit()
    return procurement

def approve_procurement(db: Session, procurement_id: int, approved_by: str):
    procurement = get_procurement(db, procurement_id)
    if not procurement:
        return None
    procurement.approval_status = "Approved"
    procurement.status = "Approved"
    procurement.approved_by = approved_by
    db.commit()
    db.refresh(procurement)
    return procurement

def reject_procurement(db: Session, procurement_id: int, approved_by: str):
    procurement = get_procurement(db, procurement_id)
    if not procurement:
        return None
    procurement.approval_status = "Rejected"
    procurement.status = "Rejected"
    procurement.approved_by = approved_by
    db.commit()
    db.refresh(procurement)
    return procurement

def filter_procurements(db: Session, status: str):
    return db.query(Procurement).filter(Procurement.status == status).all()
