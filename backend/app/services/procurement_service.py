from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

from app.models.procurement import Procurement
from app.schemas.procurement import ProcurementCreate
from sqlalchemy import or_
from sqlalchemy import asc, desc

# =====================================
# Create Procurement
# =====================================
def create_procurement(
    db: Session,
    procurement: ProcurementCreate
):

    try:

        total_price = (
            procurement.quantity *
            procurement.unit_price
        )

        new_procurement = Procurement(
            item_name=procurement.item_name,
            vendor_id=procurement.vendor_id,
            quantity=procurement.quantity,
            unit_price=procurement.unit_price,
            total_price=total_price,
            status="Pending"
        )

        db.add(new_procurement)
        db.commit()
        db.refresh(new_procurement)

        return new_procurement

    except SQLAlchemyError as e:

        db.rollback()

        print("DATABASE ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =====================================
# Get All Procurements
# =====================================
def get_all_procurements(
    db: Session
):

    return db.query(
        Procurement
    ).all()


# =====================================
# Get Procurement By ID
# =====================================
def get_procurement(
    db: Session,
    procurement_id: int
):

    return db.query(
        Procurement
    ).filter(
        Procurement.id == procurement_id
    ).first()


# =====================================
# Update Procurement
# =====================================
def update_procurement(
    db: Session,
    procurement_id: int,
    procurement: ProcurementCreate
):

    existing = db.query(
        Procurement
    ).filter(
        Procurement.id == procurement_id
    ).first()

    if existing is None:
        return None

    existing.item_name = procurement.item_name
    existing.vendor_id = procurement.vendor_id
    existing.quantity = procurement.quantity
    existing.unit_price = procurement.unit_price

    existing.total_price = (
        procurement.quantity *
        procurement.unit_price
    )

    db.commit()
    db.refresh(existing)

    return existing


# =====================================
# Delete Procurement
# =====================================
def delete_procurement(
    db: Session,
    procurement_id: int
):

    procurement = db.query(
        Procurement
    ).filter(
        Procurement.id == procurement_id
    ).first()

    if procurement is None:
        return None

    db.delete(procurement)
    db.commit()

    return procurement
# =====================================
# Approve Procurement
# =====================================

def approve_procurement(
    db: Session,
    procurement_id: int,
    approved_by: str
):

    try:

        procurement = db.query(
            Procurement
        ).filter(
            Procurement.id == procurement_id
        ).first()

        if procurement is None:
            return None

        procurement.approval_status = "Approved"
        procurement.status = "Approved"
        procurement.approved_by = approved_by

        db.commit()
        db.refresh(procurement)

        return procurement

    except SQLAlchemyError as e:

        db.rollback()

        print("DATABASE ERROR:", e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
        
def filter_procurements(
    db: Session,
    status: str
):

    procurements = db.query(
        Procurement
    ).filter(
        Procurement.status == status
    ).all()

    return procurements

# =====================================
# Reject Procurement
# =====================================
def reject_procurement(
    db: Session,
    procurement_id: int,
    approved_by: str
):

    procurement = db.query(
        Procurement
    ).filter(
        Procurement.id == procurement_id
    ).first()

    if procurement is None:
        return None

    procurement.approval_status = "Rejected"
    procurement.status = "Rejected"
    procurement.approved_by = approved_by

    db.commit()
    db.refresh(procurement)

    return procurement
from sqlalchemy import or_

# =====================================
# Search Procurement
# =====================================
def search_procurements(
    db: Session,
    keyword: str
):

    procurements = db.query(
        Procurement
    ).filter(
        or_(
            Procurement.item_name.ilike(f"%{keyword}%")
        )
    ).all()

    return procurements

def procurement_dashboard(db: Session):

    total = db.query(Procurement).count()

    approved = db.query(
        Procurement
    ).filter(
        Procurement.status == "Approved"
    ).count()

    pending = db.query(
        Procurement
    ).filter(
        Procurement.status == "Pending"
    ).count()

    rejected = db.query(
        Procurement
    ).filter(
        Procurement.status == "Rejected"
    ).count()

    return {

        "total_procurements": total,

        "approved": approved,

        "pending": pending,

        "rejected": rejected

    }

def get_procurements_paginated(

    db: Session,

    page: int = 1,

    limit: int = 10

):

    skip = (page - 1) * limit

    procurements = (

        db.query(Procurement)

        .offset(skip)

        .limit(limit)

        .all()

    )

    total = db.query(Procurement).count()

    return {

        "page": page,

        "limit": limit,

        "total": total,

        "data": procurements

    }
    
def sort_procurements(

    db: Session,

    field: str,

    order: str

):

    allowed_fields = {

        "item_name": Procurement.item_name,

        "quantity": Procurement.quantity,

        "unit_price": Procurement.unit_price,

        "status": Procurement.status

    }

    if field not in allowed_fields:

        raise HTTPException(

            status_code=400,

            detail="Invalid sort field."

        )

    column = allowed_fields[field]

    if order.lower() == "desc":

        return db.query(

            Procurement

        ).order_by(

            desc(column)

        ).all()

    return db.query(

        Procurement

    ).order_by(

        asc(column)

    ).all()