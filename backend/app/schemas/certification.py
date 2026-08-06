from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional


class CertificationCreate(BaseModel):
    vendor_id: int
    certification_name: str
    certificate_number: str
    issuing_authority: str
    issue_date: date
    expiry_date: date
    status: Optional[str] = "Active"


class CertificationUpdate(BaseModel):
    certification_name: Optional[str] = None
    certificate_number: Optional[str] = None
    issuing_authority: Optional[str] = None
    issue_date: Optional[date] = None
    expiry_date: Optional[date] = None
    status: Optional[str] = None


class CertificationResponse(CertificationCreate):
    id: int
    file_name: Optional[str] = None
    file_path: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
