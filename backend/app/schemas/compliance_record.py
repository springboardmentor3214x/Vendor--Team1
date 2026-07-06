from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional

class ComplianceRecordCreate(BaseModel):
    vendor_id: int
    compliance_type: str
    status: Optional[str] = "Pending Verification"
    verified_by: Optional[str] = None

class ComplianceRecordUpdate(BaseModel):
    status: Optional[str] = None
    verified_by: Optional[str] = None
    verification_date: Optional[date] = None


def _pending_compliance_record_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "title", "")),
            "state": getattr(item, "status", "Draft"),
            "owner": getattr(item, "created_by", None),
        })
    return rows


def _pending_compliance_record_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
        else:
            totals["other"] = totals.get("other", 0) + 1
    return totals
