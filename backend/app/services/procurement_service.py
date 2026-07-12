from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

from app.models.procurement import Procurement
from app.schemas.procurement import ProcurementCreate
from sqlalchemy import or_

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