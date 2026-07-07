from pydantic import BaseModel
from datetime import date


class ProcurementCreate(BaseModel):

    vendor_id: int

    product_name: str

    quantity: int

    unit_price: float

    order_date: date

    expected_delivery: date

    status: str