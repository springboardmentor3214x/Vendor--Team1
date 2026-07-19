from pydantic import BaseModel, ConfigDict, model_validator
from typing import Optional
from datetime import datetime


class InvoiceCreate(BaseModel):
    invoice_number: Optional[str] = None
    po_id: int
    procurement_id: int
    vendor_id: int
    vendor_name: str
    invoice_amount: float
    tax_amount: Optional[float] = 0.0
    due_date: Optional[datetime] = None
    remarks: Optional[str] = None

    @model_validator(mode='before')
    def map_frontend_aliases(cls, values):
        if isinstance(values, dict):
            if 'invoiceNumber' in values and not values.get('invoice_number'):
                values['invoice_number'] = values['invoiceNumber']
            if 'poId' in values and not values.get('po_id'):
                values['po_id'] = values['poId']
            if 'procurementId' in values and not values.get('procurement_id'):
                values['procurement_id'] = values['procurementId']
            if 'vendorId' in values and not values.get('vendor_id'):
                values['vendor_id'] = values['vendorId']
            if 'vendorName' in values and not values.get('vendor_name'):
                values['vendor_name'] = values['vendorName']
            if 'invoiceAmount' in values and not values.get('invoice_amount'):
                values['invoice_amount'] = float(values['invoiceAmount'])
            if 'taxAmount' in values and not values.get('tax_amount'):
                values['tax_amount'] = float(values['taxAmount']) if values['taxAmount'] is not None else 0.0
            if 'dueDate' in values and not values.get('due_date'):
                if values['dueDate']:
                    try:
                        values['due_date'] = datetime.fromisoformat(str(values['dueDate']).replace('Z', '+00:00'))
                    except Exception:
                        pass
        return values


class InvoiceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    invoice_number: str
    po_id: int
    procurement_id: int
    vendor_id: int
    vendor_name: str
    invoice_amount: float
    tax_amount: float
    total_amount: float
    due_date: Optional[datetime] = None
    remarks: Optional[str] = None
    file_name: Optional[str] = None
    file_path: Optional[str] = None
    payment_status: str
    verified_by: Optional[str] = None
    approved_by: Optional[str] = None
    invoice_date: Optional[datetime] = None


class InvoiceVerifyRequest(BaseModel):
    action: str
    remarks: Optional[str] = None


class InvoicePaymentStatusRequest(BaseModel):
    status: str
    remarks: Optional[str] = None
