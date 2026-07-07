from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from app.database.base import Base


class Procurement(Base):
    __tablename__ = "procurements"

    id = Column(Integer, primary_key=True, index=True)

    vendor_id = Column(Integer, ForeignKey("vendors.id"))

    product_name = Column(String)

    quantity = Column(Integer)

    unit_price = Column(Float)

    total_price = Column(Float)

    order_date = Column(Date)

    expected_delivery = Column(Date)

    status = Column(String)