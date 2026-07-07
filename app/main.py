from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import APP_TITLE, CORS_ORIGINS
from app.database.connection import engine
from app.database.base import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title=APP_TITLE)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
