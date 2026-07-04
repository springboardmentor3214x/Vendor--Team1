from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class CommunicationCreate(BaseModel):
    vendor_id: Optional[int] = None
    procurement_id: Optional[int] = None
    po_id: Optional[int] = None


def _pending_communication_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_communication_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals
