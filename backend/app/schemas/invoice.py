from pydantic import BaseModel, ConfigDict, model_validator
from typing import Optional
from datetime import datetime

class InvoiceCreate(BaseModel):
    invoice_number: Optional[str] = None
    po_id: int
    procurement_id: int
    vendor_id: int

class InvoiceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    invoice_number: str
    po_id: int
    procurement_id: int
    vendor_id: int


def _pending_invoice_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_invoice_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_invoice_rows_2(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_invoice_totals_2(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals
