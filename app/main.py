from fastapi import FastAPI
from app.database.connection import engine
from app.database.base import Base
from app.api.vendor import router as vendor_router

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Vendor Reliability Platform API")
app.include_router(vendor_router)
