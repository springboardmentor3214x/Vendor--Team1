from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database.base import Base


class Procurement(Base):
    __tablename__ = "procurements"

    id = Column(Integer, primary_key=True, index=True)

    item_name = Column(String(100), nullable=False)

    vendor_id = Column(
        Integer,
        ForeignKey("vendors.id"),
        nullable=False
    )

    quantity = Column(Integer, nullable=False)

    unit_price = Column(Float, nullable=False)

    total_price = Column(Float, nullable=False)

    status = Column(
        String(50),
        default="Pending"
    )
    approval_status = Column(
    String(50),
    default="Pending"
)

approved_by = Column(
    String(100),
    nullable=True
)