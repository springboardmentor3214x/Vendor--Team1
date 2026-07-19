from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class NotificationCreate(BaseModel):
    user_id: Optional[int] = None
    target_role: Optional[str] = None
    notification_type: str
    title: str


def _pending_notification_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_notification_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals
