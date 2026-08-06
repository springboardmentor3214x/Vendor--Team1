from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from datetime import datetime

from app.models.purchase_order import PurchaseOrder
from app.models.procurement import Procurement
from app.models.order_tracking import OrderTracking
from app.schemas.purchase_order import PurchaseOrderCreate, PurchaseOrderUpdate


def generate_po_number(db: Session) -> str:
    count = db.query(PurchaseOrder).count() + 1
    return f"PO-{datetime.utcnow().year}-{count:04d}"


def create_purchase_order(db: Session, data: PurchaseOrderCreate, approved_by: str = None):
    po_num = generate_po_number(db)
    total_cost = (data.quantity * data.unit_price) + (data.tax_amount or 0.0)

    po = PurchaseOrder(
        po_number=po_num,
        procurement_id=data.procurement_id,
        vendor_id=data.vendor_id,
        vendor_name=data.vendor_name,
        vendor_address=data.vendor_address,
        contact_person=data.contact_person,
        item_name=data.item_name,
        quantity=data.quantity,
        unit_price=data.unit_price,
        total_cost=total_cost,
        tax_amount=data.tax_amount or 0.0,
        shipping_address=data.shipping_address,
        expected_delivery_date=data.expected_delivery_date,
        payment_terms=data.payment_terms or "Net 30",
        status="Issued",
        approved_by=approved_by
    )

    try:
        db.add(po)
        # Update procurement status to Ordered
        proc = db.query(Procurement).filter(Procurement.id == data.procurement_id).first()
        if proc:
            proc.status = "Ordered"
            proc.vendor_id = data.vendor_id

        db.commit()
        db.refresh(po)

        # Automatically create initial OrderTracking record
        tracking = OrderTracking(
            po_id=po.id,
            procurement_id=po.procurement_id,
            vendor_id=po.vendor_id,
            expected_delivery_date=po.expected_delivery_date,
            delivery_status="Awaiting Shipment",
            delay_status="On Time"
        )
        db.add(tracking)
        db.commit()

        return po
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def get_all_purchase_orders(db: Session):
    return db.query(PurchaseOrder).all()


def get_purchase_order(db: Session, po_id: int):
    return db.query(PurchaseOrder).filter(PurchaseOrder.id == po_id).first()


def get_purchase_orders_by_vendor(db: Session, vendor_id: int):
    return db.query(PurchaseOrder).filter(PurchaseOrder.vendor_id == vendor_id).all()


def update_purchase_order_status(db: Session, po_id: int, status: str):
    po = get_purchase_order(db, po_id)
    if not po:
        return None
    po.status = status
    db.commit()
    db.refresh(po)
    return po
