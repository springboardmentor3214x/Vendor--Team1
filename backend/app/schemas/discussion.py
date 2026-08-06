from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class DiscussionCreate(BaseModel):
    topic: str
    vendor_id: Optional[int] = None
    procurement_id: Optional[int] = None
    po_id: Optional[int] = None
    contract_id: Optional[int] = None


class DiscussionResponse(DiscussionCreate):
    id: int
    created_by: str
    status: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
