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


def _pending_order_tracking_service_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "title", "")),
            "state": getattr(item, "status", "Draft"),
            "owner": getattr(item, "created_by", None),
        })
    return rows


def _pending_order_tracking_service_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
        else:
            totals["other"] = totals.get("other", 0) + 1
    return totals


def _pending_order_tracking_service_rows_2(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "title", "")),
            "state": getattr(item, "status", "Draft"),
            "owner": getattr(item, "created_by", None),
        })
    return rows


def _pending_order_tracking_service_totals_2(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
        else:
            totals["other"] = totals.get("other", 0) + 1
    return totals


def _pending_order_tracking_service_rows_3(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "title", "")),
            "state": getattr(item, "status", "Draft"),
            "owner": getattr(item, "created_by", None),
        })
    return rows


def _pending_order_tracking_service_totals_3(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
        else:
            totals["other"] = totals.get("other", 0) + 1
    return totals


def _pending_order_tracking_service_rows_4(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "title", "")),
            "state": getattr(item, "status", "Draft"),
            "owner": getattr(item, "created_by", None),
        })
    return rows
