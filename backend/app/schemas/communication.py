from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CommunicationCreate(BaseModel):
    vendor_id: Optional[int] = None
    procurement_id: Optional[int] = None
    po_id: Optional[int] = None
    contract_id: Optional[int] = None
    discussion_id: Optional[int] = None
    receiver_id: Optional[int] = None
    receiver_name: Optional[str] = None
    message: str


class CommunicationResponse(BaseModel):
    id: int
    vendor_id: Optional[int] = None
    procurement_id: Optional[int] = None
    po_id: Optional[int] = None
    contract_id: Optional[int] = None
    discussion_id: Optional[int] = None
    sender_id: Optional[int] = None
    sender_name: str
    receiver_id: Optional[int] = None
    receiver_name: Optional[str] = None
    message: str
    is_read: bool = False
    file_name: Optional[str] = None
    file_path: Optional[str] = None
    sent_at: Optional[datetime] = None

    class Config:
        from_attributes = True
