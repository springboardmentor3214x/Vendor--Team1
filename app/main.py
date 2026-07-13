from fastapi import FastAPI
from app.database.connection import engine
from app.database.base import Base
from app.api.vendor import router as vendor_router
from app.api.procurement import router as procurement_router

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Vendor Reliability Platform API")
app.include_router(vendor_router)
app.include_router(procurement_router)
