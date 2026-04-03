from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database import Base
from datetime import datetime

class UserReport(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    location_name = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    issue_type = Column(String)
    description = Column(String)
    reported_at = Column(DateTime, default=datetime.utcnow)
