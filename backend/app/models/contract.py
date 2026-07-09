from sqlalchemy import Column, Integer, Float, String, Date, DateTime, ForeignKey
from datetime import datetime

from app.database.base import Base


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)

    purchase_order_id = Column(
        Integer,
        ForeignKey("purchase_orders.id")
    )

    contract_number = Column(String, unique=True)

    contract_title = Column(String)

    start_date = Column(Date)

    end_date = Column(Date)

    contract_value = Column(Float)

    status = Column(String)

    terms_conditions = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )