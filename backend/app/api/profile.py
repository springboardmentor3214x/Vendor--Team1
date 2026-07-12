from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.models.user import User

from app.schemas.profile import (
    ProfileResponse,
    UpdateProfileRequest
)

from app.services.profile_service import (
    get_profile,
    update_profile
)

from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)


@router.get(
    "",
    response_model=ProfileResponse
)
def read_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return get_profile(
        db,
        current_user
    )


@router.put("")
def edit_profile(
    request: UpdateProfileRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return update_profile(
        db,
        current_user,
        request
    )