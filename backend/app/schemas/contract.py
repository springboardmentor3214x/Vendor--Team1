from pydantic import BaseModel
from datetime import date

class ContractCreate(BaseModel):
    name: str
    vendor_id: int
    start_date: date
    expiry_date: date
