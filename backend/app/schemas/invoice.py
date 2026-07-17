from pydantic import BaseModel, ConfigDict, model_validator
from typing import Optional
from datetime import datetime

class InvoiceCreate(BaseModel):
    invoice_number: Optional[str] = None
    po_id: int
    procurement_id: int
    vendor_id: int
    vendor_name: str
    invoice_amount: float

class InvoiceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    invoice_number: str
    po_id: int
    procurement_id: int
    vendor_id: int
    vendor_name: str
    invoice_amount: float
    tax_amount: float
    total_amount: float
    due_date: Optional[datetime] = None

class InvoiceVerifyRequest(BaseModel):
    action: str
    remarks: Optional[str] = None


def _pending_invoice_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "title", "")),
            "state": getattr(item, "status", "Draft"),
            "owner": getattr(item, "created_by", None),
        })
    return rows


def _pending_invoice_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
        else:
            totals["other"] = totals.get("other", 0) + 1
    return totals


def _pending_invoice_rows_2(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "title", "")),
            "state": getattr(item, "status", "Draft"),
            "owner": getattr(item, "created_by", None),
        })
    return rows
