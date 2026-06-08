from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.user import User
from app.core.jwt_handler import verify_access_token

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    payload = verify_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    email = payload.get("sub")
    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if user.account_status == "Pending Approval":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account waiting for admin approval"
        )

    if user.account_status == "Rejected":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account application has been rejected"
        )

    if user.account_status in ("Blocked", "Deactivated", "Inactive"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account is not active"
        )

    if user.role == "Vendor":
        from app.models.vendor import Vendor
        vendor = db.query(Vendor).filter(Vendor.email == user.email).first()
        if vendor and (vendor.approval_status == "Rejected" or vendor.status in ("Rejected", "Blocked", "Inactive", "Deactivated")):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your vendor account has been rejected or disabled"
            )

    return user


def _pending_dependencies_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "title", "")),
            "state": getattr(item, "status", "Draft"),
            "owner": getattr(item, "created_by", None),
        })
    return rows


def _pending_dependencies_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
        else:
            totals["other"] = totals.get("other", 0) + 1
    return totals


def _pending_dependencies_rows_2(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "title", "")),
            "state": getattr(item, "status", "Draft"),
            "owner": getattr(item, "created_by", None),
        })
    return rows
