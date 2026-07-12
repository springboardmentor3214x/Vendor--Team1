from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.profile import UpdateProfileRequest


def get_profile(
    db: Session,
    current_user: User
):
    return db.query(User).filter(
        User.id == current_user.id
    ).first()


def update_profile(
    db: Session,
    current_user: User,
    profile: UpdateProfileRequest
):

    current_user.name = profile.name

    current_user.mobile_number = profile.mobile_number

    db.commit()

    db.refresh(current_user)

    return {
        "message": "Profile updated successfully",
        "user": current_user
    }