from fastapi import APIRouter, Depends, Header, HTTPException, status
import os
from datetime import datetime, timedelta
from models.analytics import PageView, AnalyticsSummary
from services.database import get_database
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

async def verify_admin_key(x_api_key: str = Header(None)):
    if x_api_key != os.getenv("ADMIN_API_KEY"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key"
        )
    return x_api_key

@router.post("/pageview")
async def track_pageview(pageview: PageView, db=Depends(get_database)):
    pv_dict = pageview.dict()
    pv_dict["timestamp"] = datetime.now()
    await db.analytics.insert_one(pv_dict)
    return {"success": True}

@router.get("/summary", response_model=AnalyticsSummary)
async def get_analytics_summary(db=Depends(get_database), _=Depends(verify_admin_key)):
    now = datetime.now()
    today_start = datetime(now.year, now.month, now.day)
    week_start = today_start - timedelta(days=7)

    total_views = await db.analytics.count_documents({})
    today_views = await db.analytics.count_documents({"timestamp": {"$gte": today_start}})
    this_week = await db.analytics.count_documents({"timestamp": {"$gte": week_start}})
    form_submissions = await db.contacts.count_documents({})
    total_bookings = await db.bookings.count_documents({})

    # Top referrers aggregation
    pipeline = [
        {"$group": {"_id": "$referrer", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 5}
    ]
    referrers_cursor = db.analytics.aggregate(pipeline)
    top_referrers = []
    async for doc in referrers_cursor:
        if doc["_id"]:
            top_referrers.append({"name": doc["_id"], "count": doc["count"]})

    return {
        "total_views": total_views,
        "today_views": today_views,
        "top_referrers": top_referrers or [{"name": "direct", "count": total_views}],
        "form_submissions": form_submissions,
        "total_bookings": total_bookings,
        "this_week": this_week
    }
