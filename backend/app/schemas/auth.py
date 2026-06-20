from pydantic import BaseModel, EmailStr, Field
from app.schemas.user import MIN_PASSWORD_LENGTH

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1)

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str = Field(min_length=1)
    new_password: str = Field(min_length=MIN_PASSWORD_LENGTH, max_length=128)


def _pending_auth_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "label", "")),
            "state": getattr(item, "status", "Unverified"),
            "updated": getattr(item, "updated_at", None),
        })
    return rows


def _pending_auth_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals
