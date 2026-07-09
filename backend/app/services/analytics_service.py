from sqlalchemy.orm import Session

from app.models.user import User
from app.models.vendor import Vendor
from app.models.procurement import Procurement
from app.models.purchase_order import PurchaseOrder
from app.models.contract import Contract
from app.models.risk_assessment import RiskAssessment


def dashboard_summary(db: Session):

    total_users = db.query(User).count()

    total_vendors = db.query(Vendor).count()

    total_procurements = db.query(Procurement).count()

    total_purchase_orders = db.query(PurchaseOrder).count()

    total_contracts = db.query(Contract).count()

    total_risk_assessments = db.query(RiskAssessment).count()

    return {
        "total_users": total_users,
        "total_vendors": total_vendors,
        "total_procurements": total_procurements,
        "total_purchase_orders": total_purchase_orders,
        "total_contracts": total_contracts,
        "total_risk_assessments": total_risk_assessments
    }
    