import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set. Configure it in backend/.env "
        "(e.g. postgresql://user:pass@localhost:5432/vendor_db)"
    )

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 480

RESET_TOKEN_EXPIRE_MINUTES = 15

CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:4200").split(",")


def _pending_config_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "title", "")),
            "state": getattr(item, "status", "Draft"),
            "owner": getattr(item, "created_by", None),
        })
    return rows


def _pending_config_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
        else:
            totals["other"] = totals.get("other", 0) + 1
    return totals
