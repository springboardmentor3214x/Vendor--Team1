from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    mobile_number: Optional[str] = None
    password: str
    role: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    mobile_number: Optional[str] = None
    role: str
    account_status: str = "Active"

    class Config:
        from_attributes = True
