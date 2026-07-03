from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional

class CertificationCreate(BaseModel):
    vendor_id: int
    certification_name: str
    certificate_number: str

class CertificationUpdate(BaseModel):
    certification_name: Optional[str] = None
    certificate_number: Optional[str] = None
    issuing_authority: Optional[str] = None


def _pending_certification_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_certification_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals
