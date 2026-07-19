from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing import Optional, List
from datetime import datetime


class ProcurementCreate(BaseModel):
    request_title: Optional[str] = None
    department: Optional[str] = None
    requested_by: Optional[str] = None
    item_name: str = Field(min_length=1, max_length=100)
    category: Optional[str] = None
    vendor_id: Optional[int] = None
    quantity: int = Field(1, gt=0)
    unit_of_measurement: Optional[str] = "Units"
    unit_price: Optional[float] = Field(0.0, ge=0)
    estimated_budget: Optional[float] = Field(None, ge=0)
    priority: Optional[str] = "Medium"
    business_justification: Optional[str] = None
    remarks: Optional[str] = None
    supporting_document: Optional[str] = None
    expected_delivery_date: Optional[datetime] = None
    status: Optional[str] = "Pending"

    @model_validator(mode='before')
    def map_frontend_aliases(cls, values):
        if isinstance(values, dict):
            if 'requestTitle' in values and not values.get('request_title'):
                values['request_title'] = values['requestTitle']
            if 'departmentName' in values and not values.get('department'):
                values['department'] = values['departmentName']
            if 'requestedBy' in values and not values.get('requested_by'):
                values['requested_by'] = values['requestedBy']
            if 'itemName' in values and not values.get('item_name'):
                values['item_name'] = values['itemName']
            if 'productCategory' in values and not values.get('category'):
                values['category'] = values['productCategory']
            if 'unit' in values and not values.get('unit_of_measurement'):
                values['unit_of_measurement'] = values['unit']
            if 'estimatedBudget' in values and not values.get('estimated_budget'):
                values['estimated_budget'] = float(values['estimatedBudget']) if values['estimatedBudget'] is not None else None
            if 'requiredDeliveryDate' in values and not values.get('expected_delivery_date'):
                if values['requiredDeliveryDate']:
                    try:
                        values['expected_delivery_date'] = datetime.fromisoformat(str(values['requiredDeliveryDate']).replace('Z', '+00:00'))
                    except Exception:
                        pass
            if 'businessJustification' in values and not values.get('business_justification'):
                values['business_justification'] = values['businessJustification']
            if 'additionalRemarks' in values and not values.get('remarks'):
                values['remarks'] = values['additionalRemarks']
            if 'supportingDocument' in values and not values.get('supporting_document'):
                values['supporting_document'] = values['supportingDocument']
            if 'requestStatus' in values and not values.get('status'):
                values['status'] = values['requestStatus']
        return values

    @model_validator(mode='after')
    def require_justification_when_submitted(self):
        if (self.status or "Pending") != "Draft":
            if not (self.business_justification or "").strip():
                raise ValueError("Business Justification is required to submit a procurement request")
        return self


PROCUREMENT_PRIORITIES = ["Low", "Medium", "High", "Critical"]

PROCUREMENT_STATUSES = [
    "Draft", "Pending", "Approved", "Vendor Assigned", "Ordered",
    "In Transit", "Delivered", "Completed", "Cancelled", "Modification Required",
]


class ProcurementApprovalRequest(BaseModel):
    action: str
    remarks: Optional[str] = None


class ProcurementResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    request_number: Optional[str] = None
    request_title: Optional[str] = None
    department: Optional[str] = None
    requested_by: Optional[str] = None
    item_name: str
    category: Optional[str] = None
    vendor_id: Optional[int] = None
    quantity: int
    unit_of_measurement: Optional[str] = None
    unit_price: float
    total_price: float
    priority: Optional[str] = "Medium"
    business_justification: Optional[str] = None
    remarks: Optional[str] = None
    supporting_document: Optional[str] = None
    status: str
    approval_status: str
    approved_by: Optional[str] = None
    expected_delivery_date: Optional[datetime] = None
    actual_delivery_date: Optional[datetime] = None
    created_at: Optional[datetime] = None


class StatusHistoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    procurement_id: int
    po_id: Optional[int] = None
    status: str
    updated_by: str
    remarks: Optional[str] = None
    created_at: Optional[datetime] = None
