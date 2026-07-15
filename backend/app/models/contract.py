from sqlalchemy import Column, Integer, String, Date
from app.database.base import Base

class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    vendor_id = Column(Integer, nullable=False)
    start_date = Column(Date, nullable=False)
    expiry_date = Column(Date, nullable=False)
    status = Column(String(50), default="Active")
