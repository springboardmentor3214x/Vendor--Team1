from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# ===========================
# Create Document
# ===========================
class VendorDocumentCreate(BaseModel):
    document_name: str
    document_type: str
    file_path: str


# ===========================
# Response
# ===========================
class VendorDocumentResponse(BaseModel):
    id: int
    vendor_id: int
    document_name: str
    document_type: str
    file_path: str
    uploaded_at: datetime

    class Config:
        from_attributes = True