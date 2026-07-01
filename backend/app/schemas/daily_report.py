from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class DailyReportBase(BaseModel):
    report_date: datetime
    report_type: str
    data: Dict[str, Any]
    organization_id: Optional[str] = None


class DailyReportCreate(DailyReportBase):
    pass


class DailyReportUpdate(BaseModel):
    data: Optional[Dict[str, Any]] = None


class DailyReportResponse(DailyReportBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
