from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing import Optional, List
from datetime import datetime

class ProcurementCreate(BaseModel):
    request_title: Optional[str] = None
    department: Optional[str] = None
    requested_by: Optional[str] = None
    item_name: str = Field(min_length=1, max_length=100)
    category: Optional[str] = None
    vendor_id: Optional[int] = None
    quantity: int = Field(1, gt=0)
    unit_of_measurement: Optional[str] = "Units"
    unit_price: Optional[float] = Field(0.0, ge=0)
    estimated_budget: Optional[float] = Field(None, ge=0)
    priority: Optional[str] = "Medium"

PROCUREMENT_PRIORITIES = ["Low", "Medium", "High", "Critical"]

PROCUREMENT_STATUSES = [
    "Draft", "Pending", "Approved", "Vendor Assigned", "Ordered",
    "In Transit", "Delivered", "Completed", "Cancelled", "Modification Required",
]

class ProcurementApprovalRequest(BaseModel):
    action: str
    remarks: Optional[str] = None


def _pending_procurement_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "title", "")),
            "state": getattr(item, "status", "Draft"),
            "owner": getattr(item, "created_by", None),
        })
    return rows


def _pending_procurement_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
        else:
            totals["other"] = totals.get("other", 0) + 1
    return totals


def _pending_procurement_rows_2(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "title", "")),
            "state": getattr(item, "status", "Draft"),
            "owner": getattr(item, "created_by", None),
        })
    return rows


def _pending_procurement_totals_2(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
        else:
            totals["other"] = totals.get("other", 0) + 1
    return totals


def _pending_procurement_rows_3(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "title", "")),
            "state": getattr(item, "status", "Draft"),
            "owner": getattr(item, "created_by", None),
        })
    return rows
