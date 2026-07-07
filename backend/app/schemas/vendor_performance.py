from pydantic import BaseModel


class VendorPerformanceCreate(BaseModel):

    vendor_id: int

    quality_score: float

    delivery_score: float

    cost_score: float

    response_time: float