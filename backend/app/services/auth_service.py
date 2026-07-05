from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import verify_password


def login_user(db: Session, email: str, password: str):

    # Find user by email
    user = db.query(User).filter(User.email == email).first()

    # User not found
    if user is None:
        return None

    # Check password
    if not verify_password(password, user.password):
        return None

    return user