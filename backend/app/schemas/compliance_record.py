from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional


class ComplianceRecordCreate(BaseModel):
    vendor_id: int
    compliance_type: str
    status: Optional[str] = "Pending Verification"
    verified_by: Optional[str] = None
    verification_date: Optional[date] = None
    expiry_date: Optional[date] = None
    remarks: Optional[str] = None


class ComplianceRecordUpdate(BaseModel):
    status: Optional[str] = None
    verified_by: Optional[str] = None
    verification_date: Optional[date] = None
    expiry_date: Optional[date] = None
    remarks: Optional[str] = None


class ComplianceRecordResponse(ComplianceRecordCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: Optional[datetime] = None
