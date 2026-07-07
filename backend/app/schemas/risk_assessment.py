from pydantic import BaseModel


class RiskAssessmentCreate(BaseModel):
    vendor_id: int


class RiskAssessmentResponse(BaseModel):
    id: int
    vendor_id: int
    reliability_score: float
    risk_level: str
    remarks: str

    class Config:
        from_attributes = True