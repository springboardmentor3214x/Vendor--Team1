from fastapi import FastAPI

from app.database.connection import engine
from app.database.base import Base

# Models
from app.models.user import User
from app.models.vendor import Vendor
from app.models.vendor_document import VendorDocument
from app.models.procurement import Procurement

# Routers
from app.api.user import router as user_router
from app.api.auth import router as auth_router
from app.api.vendor import router as vendor_router
from app.api.vendor_document import router as vendor_document_router
from app.api.profile import router as profile_router
from app.api.procurement import router as procurement_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Vendor Reliability Platform API"
)

# Register Routers
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(vendor_router)
app.include_router(vendor_document_router)
app.include_router(profile_router)
app.include_router(procurement_router)

@app.get("/")
def home():
    return {
        "message": "Vendor Reliability Platform API is running!"
    }