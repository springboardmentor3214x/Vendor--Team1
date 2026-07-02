from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
from datetime import datetime

DELIVERY_STATUSES = ["Awaiting Shipment", "In Transit", "Delivered", "Completed"]


def _pending_order_tracking_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_order_tracking_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals
