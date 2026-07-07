from sqlalchemy.orm import Session

from app.models.vendor_performance import VendorPerformance
from app.schemas.vendor_performance import VendorPerformanceCreate


def create_performance(db: Session, performance: VendorPerformanceCreate):

    reliability = (
        performance.quality_score +
        performance.delivery_score +
        performance.cost_score +
        performance.response_time
    ) / 4

    new_performance = VendorPerformance(

        vendor_id=performance.vendor_id,

        quality_score=performance.quality_score,

        delivery_score=performance.delivery_score,

        cost_score=performance.cost_score,

        response_time=performance.response_time,

        reliability_score=reliability

    )

    db.add(new_performance)

    db.commit()

    db.refresh(new_performance)

    return new_performance