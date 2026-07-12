from pydantic import BaseModel, EmailStr
from datetime import datetime


class ProfileResponse(BaseModel):

    id: int
    name: str
    email: EmailStr
    role: str
    created_at: datetime

    class Config:
        from_attributes = True


class UpdateProfileRequest(BaseModel):

    name: str

    mobile_number: str