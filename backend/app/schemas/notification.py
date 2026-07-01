from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class NotificationBase(BaseModel):
    recipient_id: str
    title: str
    message: str
    notification_type: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class NotificationCreate(NotificationBase):
    pass


class NotificationUpdate(BaseModel):
    read: Optional[bool] = None
    sent: Optional[bool] = None


class NotificationResponse(NotificationBase):
    id: str
    read: bool
    sent: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
