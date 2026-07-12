from pydantic import BaseModel, EmailStr
from typing import Optional


class VendorCreate(BaseModel):
    vendor_name: str
    company_name: str
    email: EmailStr
    phone: str
    address: str
    category: str
    status: str = "Pending"


class VendorUpdate(BaseModel):
    vendor_name: Optional[str] = None
    company_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    category: Optional[str] = None
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