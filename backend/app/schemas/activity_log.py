from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class ActivityLogBase(BaseModel):
    action: str
    entity_type: str
    entity_id: str
    user_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ActivityLogCreate(ActivityLogBase):
    pass


class ActivityLogResponse(ActivityLogBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
