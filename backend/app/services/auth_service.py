from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from fastapi import HTTPException
from app.models.user import User
from app.schemas.user import UserCreate, AdminUserCreate
from app.core.security import hash_password, verify_password
from app.core.jwt_handler import create_reset_token
from app.core.roles import Roles
from app.core.vendor_categories import UNCATEGORIZED
from app.core.config import (
    FRONTEND_BASE_URL,
    RESET_TOKEN_EXPIRE_MINUTES,
    SMTP_CONFIGURED,
)

def register_user(db: Session, user_data: UserCreate):
    from app.core.roles import ALL_ROLES
    if user_data.role not in ALL_ROLES:
        raise HTTPException(status_code=400, detail=f"Invalid role '{user_data.role}'. Allowed roles: {ALL_ROLES}")

    if user_data.role == Roles.VENDOR and not (user_data.company_name or "").strip():
        raise HTTPException(status_code=400, detail="Company Name is required for the Vendor role")

    existing = db.query(User).filter(func.lower(User.email) == user_data.email.lower()).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(user_data.password)
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        mobile_number=user_data.mobile_number,
        employee_id=(user_data.employee_id or "").strip() or None,
        password=hashed,
        role=user_data.role,
        account_status="Pending Approval"
    )

    try:
        db.add(new_user)
        db.flush()

        if user_data.role == Roles.VENDOR:
            from app.models.vendor import Vendor
            existing_vendor = db.query(Vendor).filter(
                func.lower(Vendor.email) == user_data.email.lower()
            ).first()
            if not existing_vendor:
                new_vendor = Vendor(
                    vendor_name=user_data.name,
                    company_name=user_data.company_name.strip(),
                    email=user_data.email,
                    phone=user_data.mobile_number or "0000000000",
                    address="N/A",
                    category=UNCATEGORIZED,
                    status="Pending",
                    approval_status="Pending"
                )
                db.add(new_vendor)

        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Registration failed")

def create_user_as_admin(db: Session, data: AdminUserCreate):
    from app.core.roles import ALL_ROLES
    if data.role not in ALL_ROLES:
        raise HTTPException(status_code=400, detail=f"Invalid role '{data.role}'. Allowed roles: {ALL_ROLES}")

    if data.role == Roles.VENDOR and not (data.company_name or "").strip():
        raise HTTPException(status_code=400, detail="Company Name is required for the Vendor role")

    existing = db.query(User).filter(func.lower(User.email) == data.email.lower()).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        name=data.name,
        email=data.email,
        mobile_number=data.mobile_number,
        employee_id=(data.employee_id or "").strip() or None,
        password=hash_password(data.password),
        role=data.role,
        account_status="Active",
    )

    try:
        db.add(new_user)
        db.flush()

        if data.role == Roles.VENDOR:
            from app.models.vendor import Vendor
            existing_vendor = db.query(Vendor).filter(
                func.lower(Vendor.email) == data.email.lower()
            ).first()
            if not existing_vendor:
                db.add(Vendor(
                    vendor_name=data.name,
                    company_name=data.company_name.strip(),
                    email=data.email,
                    phone=data.mobile_number or "0000000000",
                    address="N/A",
                    category=UNCATEGORIZED,
                    status="Active",
                    approval_status="Approved",
                ))

        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="User creation failed")


def _pending_auth_service_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_auth_service_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_auth_service_rows_2(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_auth_service_totals_2(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_auth_service_rows_3(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_auth_service_totals_3(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_auth_service_rows_4(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_auth_service_totals_4(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_auth_service_rows_5(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows
