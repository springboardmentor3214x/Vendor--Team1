from pydantic import BaseModel, EmailStr, ConfigDict, Field, field_validator
from typing import Optional
from datetime import datetime
from app.core.vendor_categories import VENDOR_CATEGORIES, ALL_VENDOR_CATEGORIES

VENDOR_STATUSES = ["Active", "Pending", "Inactive", "Suspended", "Rejected", "Blocked"]

def _validate_category(value: str) -> str:
    if value not in ALL_VENDOR_CATEGORIES:
        allowed = ", ".join(VENDOR_CATEGORIES)
        raise ValueError(f"Invalid vendor category '{value}'. Allowed categories: {allowed}")
    return value

def _validate_status(value: str) -> str:
    if value not in VENDOR_STATUSES:
        raise ValueError(f"Invalid vendor status '{value}'. Allowed values: {', '.join(VENDOR_STATUSES)}")
    return value


def _pending_vendor_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_vendor_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_vendor_rows_2(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_vendor_totals_2(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_vendor_rows_3(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_vendor_totals_3(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals
