from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from datetime import datetime, timedelta
from typing import Optional

from app.models.invoice import Invoice
from app.models.purchase_order import PurchaseOrder
from app.models.procurement import Procurement
from app.schemas.invoice import InvoiceCreate, InvoiceVerifyRequest
from app.services.procurement_service import record_status_history


def generate_invoice_number(db: Session) -> str:
    from sqlalchemy import func
    year = datetime.utcnow().year
    prefix = f"INV-{year}-"
    last = (
        db.query(Invoice.invoice_number)
        .filter(Invoice.invoice_number.like(f"{prefix}%"))
        .order_by(Invoice.invoice_number.desc())
        .first()
    )
    next_seq = 1
    if last and last[0]:
        try:
            next_seq = int(last[0].rsplit("-", 1)[1]) + 1
        except (ValueError, IndexError):
            next_seq = (db.query(func.count(Invoice.id)).scalar() or 0) + 1

    while db.query(Invoice).filter(Invoice.invoice_number == f"{prefix}{next_seq:04d}").first():
        next_seq += 1
    return f"{prefix}{next_seq:04d}"


def get_vendor_for_user(db: Session, user):
    from app.models.vendor import Vendor
    from sqlalchemy import func
    if not user or not user.email:
        return None
    return db.query(Vendor).filter(func.lower(Vendor.email) == user.email.lower()).first()


def get_invoices_by_vendor(db: Session, vendor_id: int):
    return db.query(Invoice).filter(Invoice.vendor_id == vendor_id).order_by(Invoice.invoice_date.desc()).all()


def create_invoice(db: Session, data: InvoiceCreate, file_name: str = None, file_path: str = None):
    invoice_number = data.invoice_number or generate_invoice_number(db)

    existing = db.query(Invoice).filter(Invoice.invoice_number == invoice_number).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Invoice number '{invoice_number}' already exists")

    po = db.query(PurchaseOrder).filter(PurchaseOrder.id == data.po_id).first()
    if not po:
        raise HTTPException(status_code=404, detail="Associated Purchase Order not found")
    if po.status not in ("Delivered", "Completed"):
        raise HTTPException(
            status_code=400,
            detail=f"An invoice can only be raised after delivery. PO {po.po_number} is currently '{po.status}'."
        )

    total_amount = data.invoice_amount + (data.tax_amount or 0.0)

    inv = Invoice(
        invoice_number=invoice_number,
        po_id=data.po_id,
        procurement_id=data.procurement_id or po.procurement_id,
        vendor_id=data.vendor_id or po.vendor_id,
        vendor_name=data.vendor_name or po.vendor_name,
        invoice_amount=data.invoice_amount,
        tax_amount=data.tax_amount or 0.0,
        total_amount=total_amount,
        due_date=data.due_date or (datetime.utcnow() + timedelta(days=30)),
        file_name=file_name,
        file_path=file_path,
        payment_status="Pending",
        remarks=data.remarks
    )

    try:
        db.add(inv)
        db.commit()
        db.refresh(inv)

        proc = db.query(Procurement).filter(Procurement.id == inv.procurement_id).first()
        if proc:
            record_status_history(db, proc.id, proc.status, inv.vendor_name, f"Invoice {inv.invoice_number} uploaded", po_id=inv.po_id)

        return inv
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def get_all_invoices(db: Session):
    return db.query(Invoice).order_by(Invoice.invoice_date.desc()).all()


def get_invoice(db: Session, invoice_id: int):
    return db.query(Invoice).filter(Invoice.id == invoice_id).first()


INVOICE_TRANSITIONS = {
    "Pending": ["Verified", "Rejected"],
    "Verified": ["Approved", "Paid", "Rejected"],
    "Approved": ["Paid", "Rejected"],
    "Paid": [],
    "Rejected": [],
}

ACTION_TO_STATUS = {
    "verify": "Verified",
    "approve": "Approved",
    "pay": "Paid",
    "reject": "Rejected",
}

STATUS_TO_ACTION = {status: action for action, status in ACTION_TO_STATUS.items()}


def update_payment_status(db: Session, invoice_id: int, request, user_name: str):
    requested = (request.status or "").strip().capitalize()
    action = STATUS_TO_ACTION.get(requested)
    if not action:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid payment status '{request.status}'. Expected one of: {sorted(STATUS_TO_ACTION)}"
        )
    return verify_invoice(
        db,
        invoice_id,
        InvoiceVerifyRequest(action=action, remarks=request.remarks),
        user_name,
    )


def verify_invoice(db: Session, invoice_id: int, request: InvoiceVerifyRequest, user_name: str):
    inv = get_invoice(db, invoice_id)
    if not inv:
        return None

    target_status = ACTION_TO_STATUS.get(request.action.lower())
    if not target_status:
        raise HTTPException(status_code=400, detail=f"Invalid action '{request.action}'")

    allowed = INVOICE_TRANSITIONS.get(inv.payment_status, [])
    if target_status not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot {request.action} invoice in '{inv.payment_status}' status. Allowed next states: {allowed or 'none (terminal state)'}"
        )

    inv.payment_status = target_status

    if target_status == "Verified":
        inv.verified_by = user_name
    elif target_status in ("Approved", "Paid"):
        inv.approved_by = user_name
        if target_status == "Paid":
            proc = db.query(Procurement).filter(Procurement.id == inv.procurement_id).first()
            if proc:
                proc.status = "Completed"
                record_status_history(db, proc.id, "Completed", user_name, f"Invoice {inv.invoice_number} paid. Procurement completed.", po_id=inv.po_id)
            po = db.query(PurchaseOrder).filter(PurchaseOrder.id == inv.po_id).first()
            if po:
                po.status = "Completed"

    if request.remarks:
        inv.remarks = request.remarks

    db.commit()
    db.refresh(inv)

    from app.models.vendor import Vendor
    from app.services import notification_service
    vendor = db.query(Vendor).filter(Vendor.id == inv.vendor_id).first()
    notification_service.notify_invoice_status(db, inv, target_status, vendor=vendor)

    return inv
