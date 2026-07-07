from sqlalchemy.orm import Session

from app.models.procurement import Procurement
from app.schemas.procurement import ProcurementCreate


def create_procurement(db: Session, procurement: ProcurementCreate):

    total = procurement.quantity * procurement.unit_price

    new_procurement = Procurement(

        vendor_id=procurement.vendor_id,

        product_name=procurement.product_name,

        quantity=procurement.quantity,

        unit_price=procurement.unit_price,

        total_price=total,

        order_date=procurement.order_date,

        expected_delivery=procurement.expected_delivery,

        status=procurement.status

    )

    db.add(new_procurement)

    db.commit()

    db.refresh(new_procurement)

    return new_procurement


def get_all_procurements(db: Session):
    return db.query(Procurement).all()


def get_procurement(db: Session, procurement_id: int):
    return db.query(Procurement).filter(
        Procurement.id == procurement_id
    ).first()


def update_procurement(
    db: Session,
    procurement_id: int,
    procurement: ProcurementCreate
):

    existing = db.query(Procurement).filter(
        Procurement.id == procurement_id
    ).first()

    if existing is None:
        return None

    existing.vendor_id = procurement.vendor_id
    existing.product_name = procurement.product_name
    existing.quantity = procurement.quantity
    existing.unit_price = procurement.unit_price
    existing.total_price = procurement.quantity * procurement.unit_price
    existing.order_date = procurement.order_date
    existing.expected_delivery = procurement.expected_delivery
    existing.status = procurement.status

    db.commit()

    db.refresh(existing)

    return existing


def delete_procurement(db: Session, procurement_id: int):

    procurement = db.query(Procurement).filter(
        Procurement.id == procurement_id
    ).first()

    if procurement is None:
        return None

    db.delete(procurement)

    db.commit()

    return procurement