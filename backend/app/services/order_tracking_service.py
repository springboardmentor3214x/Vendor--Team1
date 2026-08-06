from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime, timezone

from app.models.order_tracking import OrderTracking
from app.models.purchase_order import PurchaseOrder
from app.models.procurement import Procurement
from app.schemas.order_tracking import OrderTrackingUpdate
from app.utils.delivery_timing import delivery_status_from_times


def get_all_tracking(db: Session):
    return db.query(OrderTracking).all()


def get_tracking_by_po(db: Session, po_id: int):
    return db.query(OrderTracking).filter(OrderTracking.po_id == po_id).first()


def update_tracking_status(db: Session, po_id: int, data: OrderTrackingUpdate):
    tracking = get_tracking_by_po(db, po_id)
    if not tracking:
        # Create if missing
        po = db.query(PurchaseOrder).filter(PurchaseOrder.id == po_id).first()
        if not po:
            return None
        tracking = OrderTracking(
            po_id=po.id,
            procurement_id=po.procurement_id,
            vendor_id=po.vendor_id,
            expected_delivery_date=po.expected_delivery_date,
            delivery_status="Awaiting Shipment",
            delay_status="On Time"
        )
        db.add(tracking)

    tracking.delivery_status = data.delivery_status
    if data.dispatch_date:
        tracking.dispatch_date = data.dispatch_date
    if data.actual_delivery_date:
        tracking.actual_delivery_date = data.actual_delivery_date

    # Evaluate delay status automatically
    now = datetime.utcnow()
    expected = tracking.expected_delivery_date or now
    actual = tracking.actual_delivery_date or now

    if expected.tzinfo is not None:
        expected = expected.replace(tzinfo=None)
    if actual.tzinfo is not None:
        actual = actual.replace(tzinfo=None)

    if tracking.delivery_status in ("In Transit", "Awaiting Shipment"):
        if now > expected:
            tracking.delay_status = "Delayed"
        else:
            tracking.delay_status = "On Time"

    elif tracking.delivery_status in ("Delivered", "Completed"):
        del_status, delay_hours, delay_days = delivery_status_from_times(expected, actual)
        tracking.delay_days = delay_days
        tracking.delay_hours = delay_hours
        tracking.delay_status = "Delayed" if delay_hours > 0 else "On Time"

    # Also update PurchaseOrder and Procurement statuses
    po = db.query(PurchaseOrder).filter(PurchaseOrder.id == po_id).first()
    if po:
        po.status = tracking.delivery_status
        proc = db.query(Procurement).filter(Procurement.id == po.procurement_id).first()
        if proc:
            proc.status = tracking.delivery_status

    db.commit()
    db.refresh(tracking)
    return tracking
