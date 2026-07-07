from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.database.base import Base


class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)

    vendor_name = Column(String(100), nullable=False)

    company_name = Column(String(100), nullable=False)

    email = Column(String(100), unique=True, nullable=False)

    phone = Column(String(20), nullable=False)

    address = Column(String(255), nullable=False)

    category = Column(String(100), nullable=False)

    status = Column(String(50), default="Active")

    created_at = Column(DateTime, default=datetime.utcnow)