from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.auth import LoginRequest
from app.database.connection import get_db
from app.services.auth_service import login_user
from app.core.jwt_handler import create_access_token

router = APIRouter()


@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):

    user = login_user(db, request.email, request.password)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid Email or Password"
        )

    # Generate JWT Token
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