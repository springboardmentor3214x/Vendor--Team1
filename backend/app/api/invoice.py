from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import shutil

from app.database.connection import get_db
from app.schemas.invoice import InvoiceCreate, InvoiceResponse, InvoiceVerifyRequest
from app.services import invoice_service
from app.core.dependencies import get_current_user, role_required
from app.core.roles import Roles
from app.models.user import User

router = APIRouter(prefix="/invoices", tags=["Invoices"])


@router.post("/upload", response_model=InvoiceResponse, status_code=201)
async def upload_invoice(
    invoice_number: str = Form(...),
    po_id: int = Form(...),
    procurement_id: int = Form(...),
    vendor_id: int = Form(...),
    vendor_name: str = Form(...),
    invoice_amount: float = Form(...),
    tax_amount: Optional[float] = Form(0.0),
    remarks: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN, Roles.VENDOR, Roles.PROCUREMENT_MANAGER]))
):
    file_name = None
    file_path = None

    if file:
        upload_dir = os.path.join("static", "invoices", str(vendor_id))
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_name = file.filename

    inv_data = InvoiceCreate(
        invoice_number=invoice_number,
        po_id=po_id,
        procurement_id=procurement_id,
        vendor_id=vendor_id,
        vendor_name=vendor_name,
        invoice_amount=invoice_amount,
        tax_amount=tax_amount or 0.0,
        remarks=remarks
    )

    return invoice_service.create_invoice(db, inv_data, file_name=file_name, file_path=file_path)


@router.get("/", response_model=List[InvoiceResponse])
def list_invoices(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
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
