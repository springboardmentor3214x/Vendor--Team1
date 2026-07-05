from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional

class ComplianceRecordCreate(BaseModel):
    vendor_id: int
    compliance_type: str
    status: Optional[str] = "Pending Verification"


def _pending_compliance_record_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_compliance_record_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals
