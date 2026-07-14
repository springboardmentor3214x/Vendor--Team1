from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import APP_TITLE, CORS_ORIGINS
from app.database.connection import engine
from app.database.base import Base
from app.models.vendor import Vendor
from app.models.procurement import Procurement
from app.models.delivery_performance import DeliveryPerformance
from app.models.quality_evaluation import QualityEvaluation
from app.models.communication_log import CommunicationLog
from app.models.service_rating import ServiceRating
from app.api.vendor import router as vendor_router
from app.api.procurement import router as procurement_router
from app.api.performance import router as performance_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title=APP_TITLE)
app.add_middleware(CORSMiddleware, allow_origins=CORS_ORIGINS, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(vendor_router)
app.include_router(procurement_router)
app.include_router(performance_router)
