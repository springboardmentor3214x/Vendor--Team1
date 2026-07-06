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
ACCESS_TOKEN_EXPIRE_MINUTES = 30
RESET_TOKEN_EXPIRE_MINUTES = 15
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:4200").split(",")
