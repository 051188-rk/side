from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class MessageBase(BaseModel):
    channel: str
    direction: str
    content: str
    customer_id: Optional[str] = None
    external_message_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class MessageCreate(MessageBase):
    pass


class MessageUpdate(BaseModel):
    content: Optional[str] = None
    read: Optional[bool] = None


class MessageResponse(MessageBase):
    id: str
    read: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
