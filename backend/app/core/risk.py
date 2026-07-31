LOW_RISK_THRESHOLD = 80.0
MEDIUM_RISK_THRESHOLD = 50.0

LOW_RISK = "Low Risk"
MEDIUM_RISK = "Medium Risk"
HIGH_RISK = "High Risk"
NOT_RATED = "Not Rated"


def calculate_risk_level(reliability_score: float, has_performance_data: bool = True) -> str:
    if not has_performance_data:
        return NOT_RATED

    score = reliability_score or 0.0
    if score >= LOW_RISK_THRESHOLD:
        return LOW_RISK
    if score >= MEDIUM_RISK_THRESHOLD:
        return MEDIUM_RISK
    return HIGH_RISK


def is_high_risk(reliability_score: float, has_performance_data: bool = True) -> bool:
    return calculate_risk_level(reliability_score, has_performance_data) == HIGH_RISK


def vendor_has_performance_data(db, vendor_id: int) -> bool:
    from app.models.delivery_performance import DeliveryPerformance
    from app.models.quality_evaluation import QualityEvaluation
    from app.models.service_rating import ServiceRating
    from app.models.communication_log import CommunicationLog

    for model in (DeliveryPerformance, QualityEvaluation, ServiceRating, CommunicationLog):
        if db.query(model.id).filter(model.vendor_id == vendor_id).first():
            return True
    return False
