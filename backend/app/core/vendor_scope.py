from typing import Optional
from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.core.roles import Roles
from app.models.user import User

def get_vendor_id_for_user(db: Session, user: User) -> Optional[int]:
    if user.role != Roles.VENDOR:
        return None

    from app.models.vendor import Vendor

    vendor = db.query(Vendor).filter(func.lower(Vendor.email) == user.email.lower()).first()
    return vendor.id if vendor else -1


def _pending_vendor_scope_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_vendor_scope_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals
