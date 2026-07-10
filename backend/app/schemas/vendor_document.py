from pydantic import BaseModel
from datetime import datetime


class VendorDocumentBase(BaseModel):
    vendor_id: int
    document_type: str


class VendorDocumentCreate(VendorDocumentBase):
    pass


class VendorDocumentResponse(VendorDocumentBase):
    id: int
    file_name: str
    file_path: str
    uploaded_at: datetime

    class Config:
        from_attributes = True