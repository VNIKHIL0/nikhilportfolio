from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class PageView(BaseModel):
    page: str
    referrer: Optional[str] = "direct"
    userAgent: str
    timestamp: datetime = Field(default_factory=datetime.now)

class ReferrerStat(BaseModel):
    name: str
    count: int

class AnalyticsSummary(BaseModel):
    total_views: int
    today_views: int
    top_referrers: List[ReferrerStat]
    form_submissions: int
    total_bookings: int
    this_week: int
