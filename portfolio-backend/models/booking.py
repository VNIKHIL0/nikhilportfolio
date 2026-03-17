from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class BookingBase(BaseModel):
    event_uri: str
    invitee_uri: str
    status: str = "scheduled"
    timestamp: datetime = Field(default_factory=datetime.now)

class BookingCreate(BookingBase):
    pass

class BookingDB(BookingBase):
    id: str = Field(..., alias="_id")

    class Config:
        populate_by_name = True
