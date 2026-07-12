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

class VendorCreate(BaseModel):
    vendor_name: str = Field(min_length=1, max_length=100)
    company_name: str = Field(min_length=1, max_length=150)
    email: EmailStr
    phone: str = Field(min_length=1, max_length=20)
    address: str = Field(min_length=1, max_length=255)
    category: str
    @field_validator("category")
    @classmethod
    def category_allowed(cls, v: str) -> str:
        return _validate_category(v)
    contact_person: Optional[str] = None
    designation: Optional[str] = None
    alternate_phone: Optional[str] = None
    gst_number: Optional[str] = None
    pan_number: Optional[str] = None
    company_registration_number: Optional[str] = None
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None

class VendorUpdate(BaseModel):
    vendor_name: Optional[str] = None
    company_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None
    @field_validator("status")
    @classmethod
    def status_allowed(cls, v: Optional[str]) -> Optional[str]:
        return v if v is None else _validate_status(v)
    contact_person: Optional[str] = None
    designation: Optional[str] = None
    alternate_phone: Optional[str] = None
    gst_number: Optional[str] = None
    pan_number: Optional[str] = None
    company_registration_number: Optional[str] = None
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None


def _pending_vendor_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "title", "")),
            "state": getattr(item, "status", "Draft"),
            "owner": getattr(item, "created_by", None),
        })
    return rows


def _pending_vendor_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
        else:
            totals["other"] = totals.get("other", 0) + 1
    return totals


def _pending_vendor_rows_2(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "title", "")),
            "state": getattr(item, "status", "Draft"),
            "owner": getattr(item, "created_by", None),
        })
    return rows


def _pending_vendor_totals_2(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
        else:
            totals["other"] = totals.get("other", 0) + 1
    return totals


def _pending_vendor_rows_3(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "title", "")),
            "state": getattr(item, "status", "Draft"),
            "owner": getattr(item, "created_by", None),
        })
    return rows
