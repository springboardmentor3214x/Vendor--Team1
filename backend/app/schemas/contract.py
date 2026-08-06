from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional


class ContractCreate(BaseModel):
    contract_title: str
    vendor_id: int
    vendor_name: Optional[str] = None
    contract_type: Optional[str] = "Master Agreement"
    procurement_category: Optional[str] = None
    start_date: date
    end_date: date
    contract_value: float
    payment_terms: Optional[str] = "Net 30"
    sla_details: Optional[str] = None
    warranty_details: Optional[str] = None
    responsible_manager: Optional[str] = None
    status: Optional[str] = "Active"


class ContractUpdate(BaseModel):
    contract_title: Optional[str] = None
    contract_type: Optional[str] = None
    procurement_category: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    contract_value: Optional[float] = None
    payment_terms: Optional[str] = None
    sla_details: Optional[str] = None
    warranty_details: Optional[str] = None
    responsible_manager: Optional[str] = None
    status: Optional[str] = None


class ContractResponse(ContractCreate):
    id: int
    contract_number: Optional[str] = None
    document_name: Optional[str] = None
    document_path: Optional[str] = None
    renewal_count: int = 0
    last_renewed_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
