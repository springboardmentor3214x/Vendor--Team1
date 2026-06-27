from pydantic import BaseModel, EmailStr, ConfigDict, Field, field_validator
from typing import Optional

MIN_PASSWORD_LENGTH = 8


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    mobile_number: Optional[str] = None
    employee_id: Optional[str] = None
    company_name: Optional[str] = None
    password: str = Field(min_length=MIN_PASSWORD_LENGTH, max_length=128)
    role: str

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Full name is required")
        return v.strip()

    @field_validator("mobile_number")
    @classmethod
    def valid_mobile(cls, v: Optional[str]) -> Optional[str]:
        if v is None or not v.strip():
            return None
        digits = "".join(ch for ch in v if ch.isdigit())
        if len(digits) < 10 or len(digits) > 15:
            raise ValueError("Mobile number must contain between 10 and 15 digits")
        return v.strip()


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    mobile_number: Optional[str] = None
    employee_id: Optional[str] = None
    role: str
    account_status: str = "Active"


class UserUpdateProfile(BaseModel):
    name: Optional[str] = None
    mobile_number: Optional[str] = None

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("Full name cannot be empty")
        return v

    @field_validator("mobile_number")
    @classmethod
    def valid_mobile(cls, v: Optional[str]) -> Optional[str]:
        if v is None or not v.strip():
            return v
        digits = "".join(ch for ch in v if ch.isdigit())
        if len(digits) < 10 or len(digits) > 15:
            raise ValueError("Mobile number must contain between 10 and 15 digits")
        return v.strip()


class AdminUserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    mobile_number: Optional[str] = None
    employee_id: Optional[str] = None
    company_name: Optional[str] = None
    password: str = Field(min_length=MIN_PASSWORD_LENGTH, max_length=128)
    role: str

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Full name is required")
        return v.strip()

    @field_validator("mobile_number")
    @classmethod
    def valid_mobile(cls, v: Optional[str]) -> Optional[str]:
        if v is None or not v.strip():
            return None
        digits = "".join(ch for ch in v if ch.isdigit())
        if len(digits) < 10 or len(digits) > 15:
            raise ValueError("Mobile number must contain between 10 and 15 digits")
        return v.strip()


class AdminUserUpdate(BaseModel):
    name: Optional[str] = None
    mobile_number: Optional[str] = None
    role: Optional[str] = None
    account_status: Optional[str] = None

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("Full name cannot be empty")
        return v

    @field_validator("mobile_number")
    @classmethod
    def valid_mobile(cls, v: Optional[str]) -> Optional[str]:
        if v is None or not v.strip():
            return v
        digits = "".join(ch for ch in v if ch.isdigit())
        if len(digits) < 10 or len(digits) > 15:
            raise ValueError("Mobile number must contain between 10 and 15 digits")
        return v.strip()


class AdminPasswordReset(BaseModel):
    new_password: str = Field(min_length=MIN_PASSWORD_LENGTH, max_length=128)
