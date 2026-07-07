from pydantic import BaseModel, EmailStr


class VendorCreate(BaseModel):
    vendor_name: str
    company_name: str
    email: EmailStr
    phone: str
    address: str
    category: str
    status: str