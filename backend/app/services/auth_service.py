from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.core.security import verify_password, hash_password
from app.core.jwt_handler import create_reset_token


# ==========================
# Login User
# ==========================

def login_user(db: Session, email: str, password: str):

    user = db.query(User).filter(
        User.email == email
    ).first()

    if user is None:
        return None

    if not verify_password(password, user.password):
        return None

    return user


# ==========================
# Forgot Password
# ==========================

def forgot_password(db: Session, email: str):

    user = db.query(User).filter(
        User.email == email
    ).first()

    if user is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not registered"
        )

    token = create_reset_token(
        user.email
    )

    return {

        "message": "Reset token generated successfully.",

        "reset_token": token

    }


# ==========================
# Reset Password
# ==========================

def reset_password(
    db: Session,
    user: User,
    new_password: str
):

    user.password = hash_password(
        new_password
    )

    db.commit()

    db.refresh(user)

    return {

        "message": "Password updated successfully."

    }