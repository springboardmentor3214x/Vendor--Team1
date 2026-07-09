from pydantic import BaseModel
from datetime import date


class ContractCreate(BaseModel):

    purchase_order_id: int

    contract_number: str

    contract_title: str

    start_date: date

    end_date: date

    contract_value: float

    status: str

    terms_conditions: str