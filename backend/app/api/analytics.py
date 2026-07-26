from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.services import analytics_service
from app.core.dependencies import get_current_user, role_required
from app.core.roles import Roles, INTERNAL_ROLES
from app.models.user import User

router = APIRouter(prefix="/analytics", tags=["Dashboard & Analytics"])

@router.get("/procurement-manager-dashboard")
def get_procurement_manager_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN, Roles.PROCUREMENT_MANAGER, Roles.SUPPLY_CHAIN_MANAGER]))
):
    return analytics_service.get_procurement_manager_dashboard_analytics(db)


def _pending_analytics_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_analytics_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_analytics_rows_2(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows
