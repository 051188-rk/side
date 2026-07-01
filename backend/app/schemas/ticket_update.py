from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TicketUpdateBase(BaseModel):
    ticket_id: str
    author_id: str
    content: str
    update_type: str = "comment"


class TicketUpdateCreate(TicketUpdateBase):
    pass


class TicketUpdateResponse(TicketUpdateBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
