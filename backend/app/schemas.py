from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReportCreate(BaseModel):
    location_name: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    issue_type: str
    description: str

class ReportOut(ReportCreate):
    id: int
    reported_at: datetime

    class Config:
        from_attributes = True

class PredictRequest(BaseModel):
    location_name: str
    date_time: Optional[str] = None # ISO format
