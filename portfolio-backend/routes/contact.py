from fastapi import APIRouter, Request, Depends, HTTPException, status
from slowapi import Limiter
from slowapi.util import get_remote_address
from datetime import datetime
from models.contact import ContactCreate
from services.database import get_database
from services.email import EmailService

router = APIRouter(prefix="/api/contact", tags=["contact"])
limiter = Limiter(key_func=get_remote_address)

@router.post("")
@limiter.limit("3/hour")
async def create_contact(request: Request, contact: ContactCreate, db=Depends(get_database)):
    # 1. Prepare data
    contact_dict = contact.dict()
    contact_dict["timestamp"] = datetime.now()
    contact_dict["status"] = "new"

    # 2. Save to MongoDB
    try:
        result = await db.contacts.insert_one(contact_dict)
        if not result.inserted_id:
            raise HTTPException(status_code=500, detail="Failed to save contact")
    except Exception as e:
        print(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database connection error")

    # 3. Send Emails (Async)
    try:
        await EmailService.send_contact_notification(contact_dict)
        await EmailService.send_auto_reply(contact_dict)
    except Exception as e:
        print(f"Email error: {e}")
        # We still return success because the contact was saved to the DB
        # In a real production app, we might use a task queue like Celery/RabbitMQ

    return {"success": True, "message": "Message received"}
