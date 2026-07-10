from pydantic import BaseModel, EmailStr
from typing import Optional


class VendorCreate(BaseModel):
    vendor_name: str
    company_name: str
    email: EmailStr
    phone: str
    address: str
    category: str


class VendorUpdate(BaseModel):
    vendor_name: Optional[str] = None
    company_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None


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
