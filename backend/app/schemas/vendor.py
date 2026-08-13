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
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    pincode: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    bank_account_number: Optional[str] = None
    ifsc_code: Optional[str] = None
    payment_terms: Optional[str] = None


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
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    pincode: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    bank_account_number: Optional[str] = None
    ifsc_code: Optional[str] = None
    payment_terms: Optional[str] = None


class VendorResponse(VendorCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: str
    approval_status: str

    created_by: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_by: Optional[str] = None
    updated_at: Optional[datetime] = None
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None

    delivery_score: float = 0.0
    quality_score: float = 0.0
    communication_score: float = 0.0
    service_score: float = 0.0
    reliability_score: float = 0.0


class VendorDocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    vendor_id: int
    document_type: str
    file_name: str
    file_path: str
    uploaded_at: datetime
