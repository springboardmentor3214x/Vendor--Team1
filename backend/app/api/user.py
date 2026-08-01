from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.connection import get_db
from app.models.user import User
from app.schemas.user import UserResponse
from app.core.dependencies import get_current_user, role_required
from app.core.roles import Roles

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/", response_model=List[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN]))
):
    return db.query(User).all()


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


@router.post("/{user_id}/block")
def block_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN]))
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
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
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}
