from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from fastapi import HTTPException
from datetime import datetime
from typing import Optional

from app.models.purchase_order import PurchaseOrder
from app.models.procurement import Procurement
from app.models.order_tracking import OrderTracking
from app.models.vendor import Vendor
from app.schemas.purchase_order import PurchaseOrderCreate, PurchaseOrderUpdate
from app.services.procurement_service import record_status_history


def generate_po_number(db: Session) -> str:
    year = datetime.utcnow().year
    prefix = f"PO-{year}-"
    last = (
        db.query(PurchaseOrder.po_number)
        .filter(PurchaseOrder.po_number.like(f"{prefix}%"))
        .order_by(PurchaseOrder.po_number.desc())
        .first()
    )
    next_seq = 1
    if last and last[0]:
        try:
            next_seq = int(last[0].rsplit("-", 1)[1]) + 1
        except (ValueError, IndexError):
            next_seq = (db.query(func.count(PurchaseOrder.id)).scalar() or 0) + 1

    while db.query(PurchaseOrder).filter(PurchaseOrder.po_number == f"{prefix}{next_seq:04d}").first():
        next_seq += 1
    return f"{prefix}{next_seq:04d}"


def create_purchase_order(db: Session, data: PurchaseOrderCreate, approved_by: str = "Procurement Manager"):
    vendor = db.query(Vendor).filter(Vendor.id == data.vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    if vendor.approval_status != "Approved":
        raise HTTPException(status_code=400, detail=f"Cannot create PO for unapproved vendor '{vendor.vendor_name}'")
    if vendor.status not in ("Active",):
        raise HTTPException(status_code=400, detail=f"Cannot create PO for vendor '{vendor.vendor_name}' — vendor is {vendor.status}")

    proc = db.query(Procurement).filter(Procurement.id == data.procurement_id).first()
    if not proc:
        raise HTTPException(status_code=404, detail="Procurement request not found")
    if proc.approval_status != "Approved" and proc.status not in ("Approved", "Vendor Assigned", "Ordered"):
        raise HTTPException(status_code=400, detail=f"Cannot create PO for unapproved procurement (status: {proc.status})")

    po_num = generate_po_number(db)
    total_cost = (data.quantity * data.unit_price) + (data.tax_amount or 0.0)

    po = PurchaseOrder(
        po_number=po_num,
        procurement_id=data.procurement_id,
        vendor_id=data.vendor_id,
        vendor_name=data.vendor_name or vendor.company_name or vendor.vendor_name,
        vendor_address=data.vendor_address or vendor.address_line_1 or vendor.address,
        contact_person=data.contact_person or vendor.contact_person or vendor.vendor_name,
        item_name=data.item_name or proc.item_name,
        quantity=data.quantity or proc.quantity,
        unit_price=data.unit_price or proc.unit_price,
        total_cost=total_cost,
        tax_amount=data.tax_amount or 0.0,
        shipping_address=data.shipping_address or "Central Receiving Bay",
        expected_delivery_date=data.expected_delivery_date or proc.expected_delivery_date,
        payment_terms=data.payment_terms or "Net 30",
        status="Issued",
        approved_by=approved_by
    )

    try:
        db.add(po)
        proc.status = "Ordered"
        proc.vendor_id = data.vendor_id

        db.commit()
        db.refresh(po)

        existing_tracking = db.query(OrderTracking).filter(OrderTracking.po_id == po.id).first()
        if not existing_tracking:
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

        record_status_history(db, proc.id, "Ordered", approved_by, f"Purchase Order {po.po_number} generated", po_id=po.id)

        from app.services import notification_service
        notification_service.notify_purchase_order_created(db, po, vendor=vendor)

        return po
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def get_all_purchase_orders(db: Session):
    return db.query(PurchaseOrder).order_by(PurchaseOrder.po_date.desc()).all()


def get_purchase_order(db: Session, po_id: int):
    return db.query(PurchaseOrder).filter(PurchaseOrder.id == po_id).first()


def get_purchase_orders_by_vendor(db: Session, vendor_id: int):
    return db.query(PurchaseOrder).filter(PurchaseOrder.vendor_id == vendor_id).order_by(PurchaseOrder.po_date.desc()).all()


PO_TRANSITIONS = {
    "Issued": ["In Transit", "Delivered", "Cancelled"],
    "In Transit": ["Delivered", "Cancelled"],
    "Delivered": ["Completed"],
    "Completed": [],
    "Cancelled": [],
}


def update_purchase_order_status(db: Session, po_id: int, status: str, user_name: str = "User"):
    po = get_purchase_order(db, po_id)
    if not po:
        return None
    if po.status != status:
        allowed = PO_TRANSITIONS.get(po.status, [])
        if status not in allowed:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot change PO status from '{po.status}' to '{status}'. Allowed transitions: {allowed or 'none (terminal state)'}"
            )
        po.status = status

        proc = db.query(Procurement).filter(Procurement.id == po.procurement_id).first()
        if proc:
            proc.status = status

        tracking = db.query(OrderTracking).filter(OrderTracking.po_id == po.id).first()
        if tracking:
            if status == "In Transit":
                tracking.delivery_status = "In Transit"
                if not tracking.dispatch_date:
                    tracking.dispatch_date = datetime.utcnow()
            elif status == "Delivered":
                tracking.delivery_status = "Delivered"
                if not tracking.actual_delivery_date:
                    tracking.actual_delivery_date = datetime.utcnow()

        db.commit()
        db.refresh(po)
        if proc:
            record_status_history(db, proc.id, status, user_name, f"PO #{po.po_number} status updated to {status}", po_id=po.id)

        if status in ("Delivered", "Completed"):
            from app.services.vendor_service import update_vendor_scores
            try:
                update_vendor_scores(db, po.vendor_id)
            except Exception as e:
                db.rollback()
                print(f"Failed to refresh vendor scores after PO {status}: {e}")

    return po
