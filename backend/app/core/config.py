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

FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL", CORS_ORIGINS[0].strip())

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_FROM = os.getenv("SMTP_FROM", SMTP_USERNAME or "no-reply@vrip.local")
SMTP_CONFIGURED = bool(SMTP_SERVER and SMTP_USERNAME and SMTP_PASSWORD)
