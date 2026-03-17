from fastapi import APIRouter, Depends, HTTPException
from models.booking import BookingCreate
from services.database import get_database
from datetime import datetime

router = APIRouter(prefix="/api/bookings", tags=["bookings"])

@router.post("")
async def log_booking(booking: BookingCreate, db=Depends(get_database)):
    booking_dict = booking.dict()
    booking_dict["timestamp"] = datetime.now()
    
    try:
        result = await db.bookings.insert_one(booking_dict)
        if not result.inserted_id:
            raise HTTPException(status_code=500, detail="Failed to log booking")
        return {"success": True, "id": str(result.inserted_id)}
    except Exception as e:
        print(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database connection error")
