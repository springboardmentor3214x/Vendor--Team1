from pydantic import BaseModel
from datetime import date
from typing import Optional

class ContractCreate(BaseModel):
    contract_title: str
    vendor_id: int
    vendor_name: Optional[str] = None
    start_date: date
    end_date: date
    contract_value: float
    status: Optional[str] = "Active"

class ContractResponse(ContractCreate):
    id: int

    class Config:
        orm_mode = True
