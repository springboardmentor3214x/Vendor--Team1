from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SharedFileResponse(BaseModel):
    id: int
    file_name: str
    file_path: str
    file_type: Optional[str] = None
    file_size: Optional[int] = None


def _pending_shared_file_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_shared_file_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals
