from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class ContactBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    service: Optional[str] = Field(None, max_length=100)
    budget: Optional[str] = Field(None, max_length=50)
    message: str = Field(..., min_length=3, max_length=2000)

class ContactCreate(ContactBase):
    pass

class ContactDB(ContactBase):
    id: str = Field(..., alias="_id")
    timestamp: datetime = Field(default_factory=datetime.now)
    status: str = "new"  # new, read, replied

    class Config:
        populate_by_name = True
