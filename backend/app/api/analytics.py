from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.services.analytics_service import dashboard_summary

router = APIRouter()


@router.get("/dashboard")
def get_dashboard(
    db: Session = Depends(get_db)
):

    return dashboard_summary(db)