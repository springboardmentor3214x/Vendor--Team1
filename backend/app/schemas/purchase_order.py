from pydantic import BaseModel
from datetime import date


class PurchaseOrderCreate(BaseModel):

    vendor_id: int

    procurement_id: int

    po_number: str

    order_date: date

    delivery_date: date

    amount: float

    status: str