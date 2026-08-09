from pydantic import BaseModel, ConfigDict, model_validator
from typing import Optional
from datetime import datetime


class PurchaseOrderCreate(BaseModel):
    procurement_id: int
    vendor_id: int
    vendor_name: str
    vendor_address: Optional[str] = None
    contact_person: Optional[str] = None
    item_name: str
    quantity: int = 1
    unit_price: float = 0.0
    tax_amount: Optional[float] = 0.0
    shipping_address: Optional[str] = None
    expected_delivery_date: Optional[datetime] = None
    payment_terms: Optional[str] = "Net 30"

    @model_validator(mode='before')
    def map_frontend_aliases(cls, values):
        if isinstance(values, dict):
            if 'prNumber' in values and not values.get('procurement_id'):
                pr_str = str(values['prNumber']).replace('PR-', '').replace('PR', '')
                if pr_str.isdigit():
                    values['procurement_id'] = int(pr_str)
            if 'vendorId' in values and not values.get('vendor_id'):
                values['vendor_id'] = values['vendorId']
            if 'vendorName' in values and not values.get('vendor_name'):
                values['vendor_name'] = values['vendorName']
            if 'vendorAddress' in values and not values.get('vendor_address'):
                values['vendor_address'] = values['vendorAddress']
            if 'contactPerson' in values and not values.get('contact_person'):
                values['contact_person'] = values['contactPerson']
            if 'productDetails' in values and not values.get('item_name'):
                values['item_name'] = values['productDetails']
            if 'unitPrice' in values and not values.get('unit_price'):
                values['unit_price'] = values['unitPrice']
            if 'taxDetails' in values and not values.get('tax_amount'):
                val = str(values['taxDetails'])
                import re
                nums = re.findall(r'\d+\.?\d*', val)
                values['tax_amount'] = float(nums[0]) if nums else 0.0
            if 'shippingAddress' in values and not values.get('shipping_address'):
                values['shipping_address'] = values['shippingAddress']
            if 'expectedDeliveryDate' in values and not values.get('expected_delivery_date'):
                if values['expectedDeliveryDate']:
                    try:
                        values['expected_delivery_date'] = datetime.fromisoformat(str(values['expectedDeliveryDate']).replace('Z', '+00:00'))
                    except Exception:
                        pass
            if 'paymentTerms' in values and not values.get('payment_terms'):
                values['payment_terms'] = values['paymentTerms']
        return values


class PurchaseOrderUpdate(BaseModel):
    status: Optional[str] = None
    expected_delivery_date: Optional[datetime] = None
    payment_terms: Optional[str] = None


class PurchaseOrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    po_number: str
    procurement_id: int
    vendor_id: int
    vendor_name: str
    vendor_address: Optional[str] = None
    contact_person: Optional[str] = None
    item_name: str
    quantity: int
    unit_price: float
    total_cost: float
    tax_amount: Optional[float] = 0.0
    shipping_address: Optional[str] = None
    expected_delivery_date: Optional[datetime] = None
    payment_terms: Optional[str] = None
    status: str
    approved_by: Optional[str] = None
    po_date: Optional[datetime] = None
