from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.risk_assessment import RiskAssessmentCreate
from app.services.risk_assessment_service import (
    create_risk_assessment,
    get_all_assessments,
    get_assessment
)

router = APIRouter()


@router.post("/risk-assessment")
def add_risk(
    risk: RiskAssessmentCreate,
    db: Session = Depends(get_db)
):

    assessment = create_risk_assessment(db, risk.vendor_id)

    if assessment is None:
        raise HTTPException(
            status_code=404,
            detail="Vendor Performance Not Found"
        )

    return assessment


@router.get("/risk-assessment")
def all_risk(db: Session = Depends(get_db)):
    return get_all_assessments(db)


@router.get("/risk-assessment/{vendor_id}")
def one_risk(
    vendor_id: int,
    db: Session = Depends(get_db)
):

    assessment = get_assessment(db, vendor_id)

    if not assessment:
        raise HTTPException(
            status_code=404,
            detail="Risk Assessment Not Found"
        )

    return assessment