from pydantic import BaseModel

class VendorCreate(BaseModel):
    name: str
    email: str
    phone: str
    category: str
    internal_notes: str = None
