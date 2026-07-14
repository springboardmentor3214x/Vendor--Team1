from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, or_
from fastapi import HTTPException
from datetime import datetime

from app.models.procurement import Procurement
from app.schemas.procurement import ProcurementCreate
from app.models.delivery_performance import DeliveryPerformance
from app.services.vendor_service import update_vendor_scores
from app.utils.delivery_timing import delivery_status_from_times


def create_procurement(db: Session, data: ProcurementCreate):
    total_price = data.quantity * data.unit_price
    proc = Procurement(
        item_name=data.item_name, vendor_id=data.vendor_id,
        quantity=data.quantity, unit_price=data.unit_price,
        total_price=total_price,
        expected_delivery_date=data.expected_delivery_date,
        status="Pending"
    )
    try:
        db.add(proc)
        db.commit()
        db.refresh(proc)
        return proc
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def get_all_procurements(db: Session):
    return db.query(Procurement).all()


def get_procurement(db: Session, procurement_id: int):
    return db.query(Procurement).filter(Procurement.id == procurement_id).first()


def update_procurement(db: Session, procurement_id: int, data: ProcurementCreate):
    proc = get_procurement(db, procurement_id)
    if not proc:
        return None
    proc.item_name = data.item_name
    proc.vendor_id = data.vendor_id
    proc.quantity = data.quantity
    proc.unit_price = data.unit_price
    proc.total_price = data.quantity * data.unit_price
    proc.expected_delivery_date = data.expected_delivery_date
    db.commit()
    db.refresh(proc)
    return proc


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
    if proc.status != "Pending":
        raise HTTPException(status_code=400, detail="Only pending requests can be approved")
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
    proc.status = "Cancelled"
    proc.approved_by = approved_by
    db.commit()
    db.refresh(proc)
    return proc


def assign_vendor(db: Session, procurement_id: int, vendor_id: int):
    proc = get_procurement(db, procurement_id)
    if not proc:
        return None
    if proc.status not in ("Approved", "Pending"):
        raise HTTPException(status_code=400, detail="Vendor can only be assigned on approved requests")
    proc.vendor_id = vendor_id
    proc.status = "Ordered"
    proc.approval_status = "Approved"
    db.commit()
    db.refresh(proc)
    return proc


def place_order(db: Session, procurement_id: int):
    proc = get_procurement(db, procurement_id)
    if not proc:
        return None
    if proc.status != "Approved":
        raise HTTPException(status_code=400, detail="Only approved requests can be ordered")
    proc.status = "Ordered"
    db.commit()
    db.refresh(proc)
    return proc


def filter_procurements(db: Session, status: str):
    return db.query(Procurement).filter(Procurement.status == status).all()


def search_procurements(db: Session, keyword: str):
    return db.query(Procurement).filter(
        or_(Procurement.item_name.ilike(f"%{keyword}%"))
    ).all()


def mark_delivered(db: Session, procurement_id: int, actual_time: datetime | None = None):
    proc = get_procurement(db, procurement_id)
    if not proc:
        return None
    if proc.status not in ("In Transit", "Ordered"):
        raise HTTPException(status_code=400, detail="Order must be in transit before delivery")
    proc.status = "Delivered"
    proc.actual_delivery_date = actual_time or datetime.utcnow()

    expected = proc.expected_delivery_date or proc.actual_delivery_date
    status, delay_hours, delay_days = delivery_status_from_times(expected, proc.actual_delivery_date)

    delivery = DeliveryPerformance(
        procurement_id=proc.id,
        vendor_id=proc.vendor_id,
        expected_date=expected,
        actual_date=proc.actual_delivery_date,
        delay_days=delay_days,
        delay_hours=delay_hours,
        delivery_status=status,
        remarks="Recorded when supply chain marked delivery"
    )
    db.add(delivery)
    db.commit()

    try:
        update_vendor_scores(db, proc.vendor_id)
    except Exception as e:
        print(f"Failed to update scores: {e}")

    db.refresh(proc)
    return proc


def dispatch_procurement(db: Session, procurement_id: int):
    proc = get_procurement(db, procurement_id)
    if not proc:
        return None
    if proc.status != "Ordered":
        raise HTTPException(status_code=400, detail="Only ordered purchase orders can be dispatched")
    proc.status = "In Transit"
    db.commit()
    db.refresh(proc)
    return proc


def mark_completed(db: Session, procurement_id: int):
    proc = get_procurement(db, procurement_id)
    if not proc:
        return None
    if proc.status != "Delivered":
        raise HTTPException(status_code=400, detail="Only delivered orders can be completed")
    proc.status = "Completed"
    db.commit()
    db.refresh(proc)
    return proc


def get_procurements_by_vendor(db: Session, vendor_id: int):
    return db.query(Procurement).filter(Procurement.vendor_id == vendor_id).all()


def procurement_dashboard(db: Session):
    total = db.query(Procurement).count()
    approved = db.query(Procurement).filter(Procurement.status == "Approved").count()
    pending = db.query(Procurement).filter(Procurement.status == "Pending").count()
    rejected = db.query(Procurement).filter(Procurement.status == "Cancelled").count()
    ordered = db.query(Procurement).filter(Procurement.status == "Ordered").count()
    delivered = db.query(Procurement).filter(Procurement.status == "Delivered").count()
    completed = db.query(Procurement).filter(Procurement.status == "Completed").count()
    total_spend = db.query(func.sum(Procurement.total_price)).filter(
        Procurement.status.in_(["Delivered", "Completed"])
    ).scalar() or 0
    return {
        "total": total, "approved": approved, "pending": pending,
        "rejected": rejected, "ordered": ordered, "delivered": delivered,
        "completed": completed, "total_spend": total_spend
    }
