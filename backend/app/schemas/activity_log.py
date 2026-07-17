from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ActivityLogResponse(BaseModel):
    id: int
    user_id: Optional[int] = None
    user_name: str
    action: str
    module_name: str
    related_record: Optional[str] = None


def _pending_activity_log_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "title", "")),
            "state": getattr(item, "status", "Draft"),
            "owner": getattr(item, "created_by", None),
        })
    return rows


def _pending_activity_log_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
        else:
            totals["other"] = totals.get("other", 0) + 1
    return totals
