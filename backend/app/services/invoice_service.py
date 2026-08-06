from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from datetime import datetime

from app.models.invoice import Invoice
from app.models.purchase_order import PurchaseOrder
from app.models.procurement import Procurement
from app.schemas.invoice import InvoiceCreate, InvoiceVerifyRequest


def create_invoice(db: Session, data: InvoiceCreate, file_name: str = None, file_path: str = None):
    # Check duplicate invoice number
    existing = db.query(Invoice).filter(Invoice.invoice_number == data.invoice_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="Invoice number already exists")

    total_amount = data.invoice_amount + (data.tax_amount or 0.0)

    inv = Invoice(
        invoice_number=data.invoice_number,
        po_id=data.po_id,
        procurement_id=data.procurement_id,
        vendor_id=data.vendor_id,
        vendor_name=data.vendor_name,
        invoice_amount=data.invoice_amount,
        tax_amount=data.tax_amount or 0.0,
        total_amount=total_amount,
        due_date=data.due_date,
        file_name=file_name,
        file_path=file_path,
        payment_status="Pending",
        remarks=data.remarks
    )

    try:
        db.add(inv)
        db.commit()
        db.refresh(inv)
        return inv
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def get_all_invoices(db: Session):
    return db.query(Invoice).all()


def get_invoice(db: Session, invoice_id: int):
    return db.query(Invoice).filter(Invoice.id == invoice_id).first()


def verify_invoice(db: Session, invoice_id: int, request: InvoiceVerifyRequest, user_name: str):
    inv = get_invoice(db, invoice_id)
    if not inv:
        return None

    if request.action == "verify":
        inv.payment_status = "Verified"
        inv.verified_by = user_name
    elif request.action == "approve":
        inv.payment_status = "Approved"
        inv.approved_by = user_name
    elif request.action == "pay":
        inv.payment_status = "Paid"
        inv.approved_by = user_name
        # Mark procurement as completed when invoice is paid
        proc = db.query(Procurement).filter(Procurement.id == inv.procurement_id).first()
        if proc:
            proc.status = "Completed"
    elif request.action == "reject":
        inv.payment_status = "Rejected"

    if request.remarks:
        inv.remarks = request.remarks

    db.commit()
    db.refresh(inv)
    return inv
