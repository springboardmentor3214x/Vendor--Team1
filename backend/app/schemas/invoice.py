from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class InvoiceCreate(BaseModel):
    invoice_number: str
    po_id: int
    procurement_id: int
    vendor_id: int
    vendor_name: str
    invoice_amount: float
    tax_amount: Optional[float] = 0.0
    due_date: Optional[datetime] = None
    remarks: Optional[str] = None


class InvoiceResponse(InvoiceCreate):
    id: int
    total_amount: float
    file_name: Optional[str] = None
    file_path: Optional[str] = None
    payment_status: str
    verified_by: Optional[str] = None
    approved_by: Optional[str] = None
    invoice_date: datetime

    class Config:
        from_attributes = True


class InvoiceVerifyRequest(BaseModel):
    action: str # "verify", "approve", "reject"
    remarks: Optional[str] = None
