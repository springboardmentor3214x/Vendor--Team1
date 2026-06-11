from pydantic import BaseModel, EmailStr, ConfigDict, Field, field_validator
from typing import Optional

MIN_PASSWORD_LENGTH = 8

class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    mobile_number: Optional[str] = None

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


def _pending_user_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_user_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_user_rows_2(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_user_totals_2(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_user_rows_3(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_user_totals_3(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals
