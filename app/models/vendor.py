from sqlalchemy import Column, Integer, String
from app.database.base import Base

class Vendor(Base):
    __tablename__ = "vendors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    category = Column(String(100), nullable=False)
    internal_notes = Column(String(255), nullable=True)
