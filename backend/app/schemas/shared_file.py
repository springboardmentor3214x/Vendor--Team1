from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SharedFileResponse(BaseModel):
    id: int
    file_name: str
    file_path: str
    file_type: Optional[str] = None
    file_size: Optional[int] = None
    uploaded_by: str
    vendor_id: Optional[int] = None
    procurement_id: Optional[int] = None
    po_id: Optional[int] = None
    contract_id: Optional[int] = None
    discussion_id: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
