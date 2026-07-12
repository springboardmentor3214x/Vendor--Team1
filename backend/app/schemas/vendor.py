from pydantic import BaseModel, EmailStr
from typing import Optional


class VendorCreate(BaseModel):
    vendor_name: str
    company_name: str
    email: EmailStr
    phone: str
    address: str
    category: str

    delivery_score: int = 0
    quality_score: int = 0
    compliance_score: int = 0
    communication_score: int = 0

    status: str = "Pending"


class VendorUpdate(BaseModel):
    vendor_name: Optional[str] = None
    company_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    category: Optional[str] = None

    delivery_score: Optional[int] = None
    quality_score: Optional[int] = None
    compliance_score: Optional[int] = None
    communication_score: Optional[int] = None

    status: Optional[str] = None


class VendorResponse(BaseModel):
    id: int
    vendor_name: str
    company_name: str
    email: EmailStr
    phone: str
    address: str
    category: str
    status: str
    approval_status: str
    approved_by: Optional[str]

    class Config:
        from_attributes = True


class VendorScoreUpdate(BaseModel):
    delivery_score: int
    quality_score: int
    compliance_score: int
    communication_score: int