from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.connection import get_db
from app.models.user import User
from app.schemas.user import (
    UserResponse, UserUpdateProfile,
    AdminUserCreate, AdminUserUpdate, AdminPasswordReset,
)
from app.core.dependencies import get_current_user, role_required
from app.core.roles import Roles, ALL_ROLES
from app.core.security import hash_password

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
def get_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.mobile_number and current_user.role == Roles.VENDOR:
        from app.models.vendor import Vendor
        vendor = db.query(Vendor).filter(Vendor.email == current_user.email).first()
        if vendor and vendor.phone:
            current_user.mobile_number = vendor.phone
    return current_user


@router.put("/me", response_model=UserResponse)
def update_profile(
    data: UserUpdateProfile,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if data.name is not None:
        current_user.name = data.name.strip()
    if data.mobile_number is not None:
        current_user.mobile_number = data.mobile_number.strip()
        if current_user.role == Roles.VENDOR:
            from app.models.vendor import Vendor
            vendor = db.query(Vendor).filter(Vendor.email == current_user.email).first()
            if vendor:
                vendor.phone = current_user.mobile_number
    db.commit()
    db.refresh(current_user)
    return current_user


@router.get("/", response_model=List[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN]))
):
    return db.query(User).all()


@router.post("/", response_model=UserResponse, status_code=201)
def create_user(
    data: AdminUserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN]))
):
    from app.services.auth_service import create_user_as_admin
    return create_user_as_admin(db, data)


@router.get("/recipients", response_model=List[UserResponse])
def list_recipients(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(User).filter(User.account_status == "Active").order_by(User.name.asc()).all()


def sync_vendor_status_by_email(db: Session, email: str, status: str, approval_status: str = None):
    from app.models.vendor import Vendor
    vendor = db.query(Vendor).filter(Vendor.email == email).first()
    if vendor:
        vendor.status = status
        if approval_status:
            vendor.approval_status = approval_status


@router.post("/{user_id}/approve")
def approve_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN]))
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.account_status = "Active"
    sync_vendor_status_by_email(db, user.email, "Active", "Approved")
    db.commit()
    return {"message": "User approved"}


@router.post("/{user_id}/reject")
def reject_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN]))
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.account_status = "Rejected"
    sync_vendor_status_by_email(db, user.email, "Rejected", "Rejected")
    db.commit()
    return {"message": "User rejected"}


def _check_vendor_user_activities(db: Session, user: User):
    if user.role == Roles.VENDOR:
        from app.models.vendor import Vendor
        vendor = db.query(Vendor).filter(Vendor.email == user.email).first()
        if vendor:
            from app.services.vendor_service import check_vendor_active_activities
            check_vendor_active_activities(db, vendor.id)


@router.post("/{user_id}/block")
def block_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN]))
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot block your own account")
    _check_vendor_user_activities(db, user)
    user.account_status = "Blocked"
    sync_vendor_status_by_email(db, user.email, "Blocked", "Rejected")
    db.commit()
    return {"message": "User blocked"}


@router.post("/{user_id}/deactivate")
def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN]))
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot deactivate your own account")
    _check_vendor_user_activities(db, user)
    user.account_status = "Deactivated"
    sync_vendor_status_by_email(db, user.email, "Inactive")
    db.commit()
    return {"message": "User deactivated"}


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN]))
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
    _check_vendor_user_activities(db, user)
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    data: AdminUserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN]))
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.id == current_user.id:
        if data.role is not None and data.role != user.role:
            raise HTTPException(status_code=400, detail="You cannot change your own role")
        if data.account_status is not None and data.account_status != user.account_status:
            raise HTTPException(status_code=400, detail="You cannot change your own account status")

    if data.name is not None:
        user.name = data.name.strip()
    if data.mobile_number is not None:
        user.mobile_number = data.mobile_number.strip() or None

    if data.role is not None:
        if data.role not in ALL_ROLES:
            raise HTTPException(status_code=400, detail=f"Invalid role '{data.role}'. Allowed roles: {ALL_ROLES}")
        user.role = data.role

    if data.account_status is not None:
        user.account_status = data.account_status
        vendor_status = {
            "Active": "Active", "Blocked": "Blocked",
            "Deactivated": "Inactive", "Rejected": "Rejected",
        }.get(data.account_status)
        if vendor_status:
            sync_vendor_status_by_email(db, user.email, vendor_status)

    db.commit()
    db.refresh(user)
    return user


@router.post("/{user_id}/reset-password")
def reset_user_password(
    user_id: int,
    data: AdminPasswordReset,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN]))
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.password = hash_password(data.new_password)
    db.commit()
    return {"message": f"Password reset for {user.name}"}
