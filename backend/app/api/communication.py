from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.communication import Communication
from app.schemas.communication import CommunicationCreate
from datetime import datetime

router = APIRouter(prefix="/communications", tags=["Communications"])

@router.get("/")
def get_communications(db: Session = Depends(get_db)):
    return db.query(Communication).all()

@router.post("/")
def create_communication(data: CommunicationCreate, db: Session = Depends(get_db)):
    comm = Communication(**data.dict(), sent_at=datetime.utcnow())
    db.add(comm)
    db.commit()
    return comm
