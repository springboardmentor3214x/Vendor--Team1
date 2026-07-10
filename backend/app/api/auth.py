from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.schemas.auth import (
    LoginRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest
)

from app.services.auth_service import (
    login_user,
    forgot_password,
    reset_password
)

from app.core.jwt_handler import (
    create_access_token,
    verify_reset_token
)

from app.models.user import User

router = APIRouter()


@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):

    user = login_user(db, request.email, request.password)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid Email or Password"
        )

    token = create_access_token(
        {
            "sub": user.email,
            "role": user.role
        }
    )

    return {
        "message": "Login Successful",
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    }


@router.post("/forgot-password")
def forgot_password_api(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):

    return forgot_password(db, request.email)


@router.post("/reset-password")
def reset_password_api(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):

    payload = verify_reset_token(request.token)

    if payload is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid or Expired Token"
        )

    user = db.query(User).filter(
        User.email == payload["sub"]
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User Not Found"
        )

    return reset_password(
        db,
        user,
        request.new_password
    )