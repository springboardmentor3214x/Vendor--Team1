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


def _pending_invoice_service_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "title", "")),
            "state": getattr(item, "status", "Draft"),
            "owner": getattr(item, "created_by", None),
        })
    return rows


def _pending_invoice_service_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
        else:
            totals["other"] = totals.get("other", 0) + 1
    return totals


def _pending_invoice_service_rows_2(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "title", "")),
            "state": getattr(item, "status", "Draft"),
            "owner": getattr(item, "created_by", None),
        })
    return rows


def _pending_invoice_service_totals_2(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
        else:
            totals["other"] = totals.get("other", 0) + 1
    return totals


def _pending_invoice_service_rows_3(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "title", "")),
            "state": getattr(item, "status", "Draft"),
            "owner": getattr(item, "created_by", None),
        })
    return rows


def _pending_invoice_service_totals_3(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
        else:
            totals["other"] = totals.get("other", 0) + 1
    return totals


def _pending_invoice_service_rows_4(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "title", "")),
            "state": getattr(item, "status", "Draft"),
            "owner": getattr(item, "created_by", None),
        })
    return rows


def _pending_invoice_service_totals_4(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
        else:
            totals["other"] = totals.get("other", 0) + 1
    return totals
