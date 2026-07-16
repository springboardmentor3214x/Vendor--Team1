from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime, timezone
from typing import Optional

from app.models.order_tracking import OrderTracking
from app.models.purchase_order import PurchaseOrder
from app.models.procurement import Procurement
from app.schemas.order_tracking import OrderTrackingUpdate
from app.utils.delivery_timing import delivery_status_from_times
from app.services.procurement_service import record_status_history


PO_STATUS_FOR_DELIVERY = {
    "Awaiting Shipment": "Issued",
    "In Transit": "In Transit",
    "Delivered": "Delivered",
    "Completed": "Completed",
}

PROCUREMENT_STATUS_FOR_DELIVERY = {
    "Awaiting Shipment": "Ordered",
    "In Transit": "In Transit",
    "Delivered": "Delivered",
    "Completed": "Completed",
}


def get_all_tracking(db: Session):
    records = db.query(OrderTracking).order_by(OrderTracking.updated_at.desc()).all()
    now = datetime.utcnow()
    for r in records:
        po = db.query(PurchaseOrder).filter(PurchaseOrder.id == r.po_id).first()
        if po:
            setattr(r, 'po_number', po.po_number)
            if not r.expected_delivery_date and po.expected_delivery_date:
                r.expected_delivery_date = po.expected_delivery_date
        if r.delivery_status in ("Awaiting Shipment", "In Transit") and r.expected_delivery_date:
            exp = r.expected_delivery_date.replace(tzinfo=None) if r.expected_delivery_date.tzinfo else r.expected_delivery_date
            if now > exp:
                r.delay_status = "Delayed"
            else:
                r.delay_status = "On Time"
    return records


def get_tracking_by_po(db: Session, po_id: int):
    tracking = db.query(OrderTracking).filter(OrderTracking.po_id == po_id).first()
    if not tracking:
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
        db.commit()
        db.refresh(tracking)
    po = db.query(PurchaseOrder).filter(PurchaseOrder.id == tracking.po_id).first()
    if po:
        setattr(tracking, 'po_number', po.po_number)
        if not tracking.expected_delivery_date and po.expected_delivery_date:
            tracking.expected_delivery_date = po.expected_delivery_date

    now = datetime.utcnow()
    if tracking.delivery_status in ("Awaiting Shipment", "In Transit") and tracking.expected_delivery_date:
        exp = tracking.expected_delivery_date.replace(tzinfo=None) if tracking.expected_delivery_date.tzinfo else tracking.expected_delivery_date
        if now > exp:
            tracking.delay_status = "Delayed"
        else:
            tracking.delay_status = "On Time"
    return tracking


def update_tracking_status(db: Session, po_id: int, data: OrderTrackingUpdate, user_name: str = "User"):
    tracking = get_tracking_by_po(db, po_id)
    if not tracking:
        return None

    tracking.delivery_status = data.delivery_status
    if data.dispatch_date:
        tracking.dispatch_date = data.dispatch_date
    elif data.delivery_status == "In Transit" and not tracking.dispatch_date:
        tracking.dispatch_date = datetime.utcnow()

    if data.actual_delivery_date:
        tracking.actual_delivery_date = data.actual_delivery_date
    elif data.delivery_status in ("Delivered", "Completed") and not tracking.actual_delivery_date:
        tracking.actual_delivery_date = datetime.utcnow()

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

    po = db.query(PurchaseOrder).filter(PurchaseOrder.id == po_id).first()
    if po:
        po_status = PO_STATUS_FOR_DELIVERY.get(tracking.delivery_status)
        if po_status:
            po.status = po_status

        proc = db.query(Procurement).filter(Procurement.id == po.procurement_id).first()
        if proc:
            proc_status = PROCUREMENT_STATUS_FOR_DELIVERY.get(tracking.delivery_status)
            if proc_status:
                proc.status = proc_status
            if tracking.delivery_status == "Delivered":
                proc.actual_delivery_date = tracking.actual_delivery_date
            record_status_history(
                db, proc.id, proc_status or proc.status, user_name,
                f"Delivery status updated to {tracking.delivery_status}", po_id=po.id
            )

    db.commit()

    if tracking.delivery_status in ("Delivered", "Completed") and tracking.actual_delivery_date:
        _record_delivery_performance(db, tracking, expected, actual)

    db.refresh(tracking)
    if po:
        setattr(tracking, 'po_number', po.po_number)
    return tracking


def _record_delivery_performance(db: Session, tracking: OrderTracking, expected: datetime, actual: datetime):
    from app.models.delivery_performance import DeliveryPerformance
    from app.services.vendor_service import update_vendor_scores

    existing = db.query(DeliveryPerformance).filter(
        DeliveryPerformance.procurement_id == tracking.procurement_id,
        DeliveryPerformance.vendor_id == tracking.vendor_id
    ).first()

    if not existing:
        status, delay_hours, delay_days = delivery_status_from_times(expected, actual)
        db.add(DeliveryPerformance(
            procurement_id=tracking.procurement_id,
            vendor_id=tracking.vendor_id,
            expected_date=expected,
            actual_date=actual,
            delay_days=delay_days,
            delay_hours=delay_hours,
            delivery_status=status,
            remarks="Recorded automatically on delivery status update"
        ))
        db.commit()

    try:
        update_vendor_scores(db, tracking.vendor_id)
    except Exception as e:
        db.rollback()
        print(f"Failed to refresh vendor scores after delivery: {e}")
