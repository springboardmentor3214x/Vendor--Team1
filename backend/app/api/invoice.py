from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import os

from app.database.connection import get_db
from app.schemas.invoice import (
    InvoiceCreate,
    InvoiceResponse,
    InvoiceVerifyRequest,
    InvoicePaymentStatusRequest,
)
from app.services import invoice_service
from app.core.dependencies import get_current_user, role_required
from app.core.roles import Roles
from app.models.user import User
from app.utils.uploads import (
    validate_upload,
    ALLOWED_DOCUMENT_EXTENSIONS,
    MAX_DOCUMENT_SIZE_BYTES,
)

router = APIRouter(prefix="/invoices", tags=["Invoices"])


def resolve_invoice_vendor(db: Session, current_user: User, po_id: int, vendor_id: Optional[int]) -> Optional[int]:
    if current_user.role != Roles.VENDOR:
        return vendor_id

    from app.models.purchase_order import PurchaseOrder

    vendor = invoice_service.get_vendor_for_user(db, current_user)
    if not vendor:
        raise HTTPException(status_code=403, detail="No vendor profile is linked to this account")

    po = db.query(PurchaseOrder).filter(PurchaseOrder.id == po_id).first()
    if not po:
        raise HTTPException(status_code=404, detail="Associated Purchase Order not found")
    if po.vendor_id != vendor.id:
        raise HTTPException(status_code=403, detail="You can only raise invoices against your own purchase orders")

    return vendor.id


@router.post("/upload", response_model=InvoiceResponse, status_code=201)
async def upload_invoice(
    invoice_number: Optional[str] = Form(None),
    po_id: int = Form(...),
    procurement_id: Optional[int] = Form(None),
    vendor_id: Optional[int] = Form(None),
    vendor_name: Optional[str] = Form(None),
    invoice_amount: float = Form(...),
    tax_amount: Optional[float] = Form(0.0),
    remarks: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN, Roles.VENDOR, Roles.PROCUREMENT_MANAGER, Roles.FINANCE_OFFICER]))
):
    vendor_id = resolve_invoice_vendor(db, current_user, po_id, vendor_id)

    file_name = None
    file_path = None

    if file and file.filename:
        contents = validate_upload(file, ALLOWED_DOCUMENT_EXTENSIONS, MAX_DOCUMENT_SIZE_BYTES)
        upload_dir = os.path.join("static", "invoices", str(vendor_id or 1))
        os.makedirs(upload_dir, exist_ok=True)
        file_name = os.path.basename(file.filename)
        file_path = os.path.join(upload_dir, file_name)
        with open(file_path, "wb") as buffer:
            buffer.write(contents)

    inv_data = InvoiceCreate(
        invoice_number=invoice_number or invoice_service.generate_invoice_number(db),
        po_id=po_id,
        procurement_id=procurement_id or 0,
        vendor_id=vendor_id or 0,
        vendor_name=vendor_name or "Vendor",
        invoice_amount=invoice_amount,
        tax_amount=tax_amount or 0.0,
        remarks=remarks
    )

    return invoice_service.create_invoice(db, inv_data, file_name=file_name, file_path=file_path)


@router.post("/", response_model=InvoiceResponse, status_code=201)
def create_invoice_json(
    data: InvoiceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN, Roles.VENDOR, Roles.PROCUREMENT_MANAGER, Roles.FINANCE_OFFICER]))
):
    data.vendor_id = resolve_invoice_vendor(db, current_user, data.po_id, data.vendor_id)
    return invoice_service.create_invoice(db, data)


@router.get("/", response_model=List[InvoiceResponse])
def list_invoices(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == Roles.VENDOR:
        vendor = invoice_service.get_vendor_for_user(db, current_user)
        return invoice_service.get_invoices_by_vendor(db, vendor.id) if vendor else []
    return invoice_service.get_all_invoices(db)


@router.get("/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    inv = invoice_service.get_invoice(db, invoice_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")
    if current_user.role == Roles.VENDOR:
        vendor = invoice_service.get_vendor_for_user(db, current_user)
        if not vendor or inv.vendor_id != vendor.id:
            raise HTTPException(status_code=403, detail="You can only view your own invoices")
    return inv


@router.post("/{invoice_id}/verify", response_model=InvoiceResponse)
def verify_invoice_status(
    invoice_id: int,
    request: InvoiceVerifyRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN, Roles.FINANCE_OFFICER]))
):
    inv = invoice_service.verify_invoice(db, invoice_id, request, current_user.name)
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return inv


@router.post("/{invoice_id}/payment-status", response_model=InvoiceResponse)
def update_invoice_payment_status(
    invoice_id: int,
    request: InvoicePaymentStatusRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN, Roles.FINANCE_OFFICER]))
):
    inv = invoice_service.update_payment_status(
        db, invoice_id, request, current_user.name
    )
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return inv
