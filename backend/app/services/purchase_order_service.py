from sqlalchemy.orm import Session

from app.models.purchase_order import PurchaseOrder
from app.schemas.purchase_order import PurchaseOrderCreate


def create_purchase_order(db: Session, purchase: PurchaseOrderCreate):

    new_purchase = PurchaseOrder(

        vendor_id=purchase.vendor_id,

        procurement_id=purchase.procurement_id,

        po_number=purchase.po_number,

        order_date=purchase.order_date,

        delivery_date=purchase.delivery_date,

        amount=purchase.amount,

        status=purchase.status

    )

    db.add(new_purchase)

    db.commit()

    db.refresh(new_purchase)

    return new_purchase


def get_all_purchase_orders(db: Session):

    return db.query(PurchaseOrder).all()


def get_purchase_order(db: Session, purchase_id: int):

    return db.query(PurchaseOrder).filter(
        PurchaseOrder.id == purchase_id
    ).first()


def update_purchase_order(
    db: Session,
    purchase_id: int,
    purchase: PurchaseOrderCreate
):

    existing = db.query(PurchaseOrder).filter(
        PurchaseOrder.id == purchase_id
    ).first()

    if existing is None:

        return None

    existing.vendor_id = purchase.vendor_id

    existing.procurement_id = purchase.procurement_id

    existing.po_number = purchase.po_number

    existing.order_date = purchase.order_date

    existing.delivery_date = purchase.delivery_date

    existing.amount = purchase.amount

    existing.status = purchase.status

    db.commit()

    db.refresh(existing)

    return existing


def delete_purchase_order(
    db: Session,
    purchase_id: int
):

    purchase = db.query(PurchaseOrder).filter(
        PurchaseOrder.id == purchase_id
    ).first()

    if purchase is None:

        return None

    db.delete(purchase)

    db.commit()

    return purchase