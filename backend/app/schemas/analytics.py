from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class AnalyticsBase(BaseModel):
    metric_name: str
    metric_value: float
    dimensions: Dict[str, Any] = Field(default_factory=dict)
    timestamp: Optional[datetime] = None


class AnalyticsCreate(AnalyticsBase):
    pass


class AnalyticsResponse(AnalyticsBase):
    id: str
    timestamp: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AnalyticsQuery(BaseModel):
    metric_name: str
    start_date: datetime
    end_date: datetime
    aggregation: str = "sum"
