from fastapi import APIRouter, Depends, Header, HTTPException, status
from bson import ObjectId
import os
from typing import List
from models.contact import ContactDB
from services.database import get_database
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/api/admin", tags=["admin"])

async def verify_admin_key(x_api_key: str = Header(None)):
    if x_api_key != os.getenv("ADMIN_API_KEY"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key"
        )
    return x_api_key

@router.get("/contacts", response_model=List[ContactDB])
async def get_all_contacts(db=Depends(get_database), _=Depends(verify_admin_key)):
    cursor = db.contacts.find().sort("timestamp", -1)
    contacts = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        contacts.append(doc)
    return contacts

@router.get("/contacts/{contact_id}", response_model=ContactDB)
async def get_contact_detail(contact_id: str, db=Depends(get_database), _=Depends(verify_admin_key)):
    try:
        doc = await db.contacts.find_one({"_id": ObjectId(contact_id)})
        if not doc:
            raise HTTPException(status_code=404, detail="Contact not found")
        doc["_id"] = str(doc["_id"])
        return doc
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

@router.patch("/contacts/{contact_id}")
async def update_contact_status(contact_id: str, status: str, db=Depends(get_database), _=Depends(verify_admin_key)):
    if status not in ["new", "read", "replied"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    result = await db.contacts.update_one(
        {"_id": ObjectId(contact_id)},
        {"$set": {"status": status}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"success": True}

@router.delete("/contacts/{contact_id}")
async def delete_contact(contact_id: str, db=Depends(get_database), _=Depends(verify_admin_key)):
    result = await db.contacts.delete_one({"_id": ObjectId(contact_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"success": True}
@router.get("/bookings")
async def get_all_bookings(db=Depends(get_database), _=Depends(verify_admin_key)):
    cursor = db.bookings.find().sort("timestamp", -1)
    bookings = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        bookings.append(doc)
    return bookings
