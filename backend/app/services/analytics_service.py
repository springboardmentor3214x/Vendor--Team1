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
def vendor_analytics(db: Session):

    total_vendors = db.query(Vendor).count()

    active_vendors = db.query(Vendor).filter(
        Vendor.status == "Active"
    ).count()

    pending_vendors = db.query(Vendor).filter(
        Vendor.status == "Pending"
    ).count()

    inactive_vendors = db.query(Vendor).filter(
        Vendor.status == "Inactive"
    ).count()

    suspended_vendors = db.query(Vendor).filter(
        Vendor.status == "Suspended"
    ).count()

    rejected_vendors = db.query(Vendor).filter(
        Vendor.status == "Rejected"
    ).count()

    return {

        "total_vendors": total_vendors,

        "active_vendors": active_vendors,

        "pending_vendors": pending_vendors,

        "inactive_vendors": inactive_vendors,

        "suspended_vendors": suspended_vendors,

        "rejected_vendors": rejected_vendors

    }

def procurement_analytics(db: Session):

    total_procurements = db.query(Procurement).count()

    pending_procurements = db.query(Procurement).filter(
        Procurement.status == "Pending"
    ).count()

    completed_procurements = db.query(Procurement).filter(
        Procurement.status == "Completed"
    ).count()

    cancelled_procurements = db.query(Procurement).filter(
        Procurement.status == "Cancelled"
    ).count()

    return {

        "total_procurements": total_procurements,

        "pending_procurements": pending_procurements,

        "completed_procurements": completed_procurements,

        "cancelled_procurements": cancelled_procurements

    }