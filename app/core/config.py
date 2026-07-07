import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./vendor_db.db")
CORS_ORIGINS: list[str] = os.getenv("CORS_ORIGINS", "http://localhost:4200").split(",")
APP_TITLE: str = os.getenv("APP_TITLE", "Vendor Reliability Platform API")
