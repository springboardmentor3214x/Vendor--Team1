from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class VendorCreate(BaseModel):
    vendor_name: str
    company_name: str
    email: EmailStr
    phone: str
    address: str
    category: str

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
    id: int
    status: str
    approval_status: str
    approved_by: Optional[str] = None
    delivery_score: float = 0.0
    quality_score: float = 0.0
    communication_score: float = 0.0
    service_score: float = 0.0
    reliability_score: float = 0.0

    class Config:
        from_attributes = True


class VendorDocumentResponse(BaseModel):
    id: int
    vendor_id: int
    document_type: str
    file_name: str
    file_path: str
    uploaded_at: datetime

    class Config:
        from_attributes = True
