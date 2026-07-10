from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime

from app.database.base import Base


class VendorDocument(Base):
    __tablename__ = "vendor_documents"

    id = Column(Integer, primary_key=True, index=True)

    vendor_id = Column(Integer, ForeignKey("vendors.id"))

    document_type = Column(String)

    file_name = Column(String)

    file_path = Column(String)

    uploaded_at = Column(DateTime, default=datetime.utcnow)