from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password
from app.core.jwt_handler import create_reset_token
from app.core.roles import Roles


def register_user(db: Session, user_data: UserCreate):
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(user_data.password)
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        mobile_number=user_data.mobile_number,
        password=hashed,
        role=user_data.role,
        account_status="Pending Approval"
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Registration failed")


def login_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        return None
    if user.account_status == "Pending Approval":
        raise HTTPException(status_code=403, detail="Account waiting for admin approval")
    if user.account_status in ("Blocked", "Deactivated"):
        raise HTTPException(status_code=403, detail="Account is not active")
    return user


def forgot_password(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    token = create_reset_token(email)
    return {"message": "Password reset token generated", "reset_token": token}


def reset_password(db: Session, user: User, new_password: str):
    user.password = hash_password(new_password)
    db.commit()
    return {"message": "Password has been reset successfully"}
