from pydantic import BaseModel
from datetime import datetime

class CommunicationCreate(BaseModel):
    procurement_id: int
    sender: str
    message: str
