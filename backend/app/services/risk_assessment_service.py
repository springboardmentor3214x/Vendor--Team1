from sqlalchemy.orm import Session

from app.models.vendor_performance import VendorPerformance
from app.models.risk_assessment import RiskAssessment


def create_risk_assessment(db: Session, vendor_id: int):

    performance = (
        db.query(VendorPerformance)
        .filter(VendorPerformance.vendor_id == vendor_id)
        .first()
    )

    if performance is None:
        return None

    reliability = performance.reliability_score

    if reliability >= 90:
        risk = "Low Risk"
        remarks = "Excellent Vendor"

    elif reliability >= 70:
        risk = "Medium Risk"
        remarks = "Needs Monitoring"

    else:
        risk = "High Risk"
        remarks = "High Procurement Risk"

    assessment = RiskAssessment(
        vendor_id=vendor_id,
        reliability_score=reliability,
        risk_level=risk,
        remarks=remarks
    )

    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    return assessment


def get_all_assessments(db: Session):
    return db.query(RiskAssessment).all()


def get_assessment(db: Session, vendor_id: int):
    return (
        db.query(RiskAssessment)
        .filter(RiskAssessment.vendor_id == vendor_id)
        .all()
    )