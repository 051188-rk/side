from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class TicketBase(BaseModel):
    title: str
    description: str
    category: str
    severity: str
    priority_score: float
    suggested_owner: Optional[str] = None
    labels: List[str] = Field(default_factory=list)
    affected_feature: Optional[str] = None
    reproduction_steps: List[str] = Field(default_factory=list)
    related_tickets: List[str] = Field(default_factory=list)
    organization_id: Optional[str] = None


class TicketCreate(TicketBase):
    pass


class TicketUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    severity: Optional[str] = None
    priority_score: Optional[float] = None
    suggested_owner: Optional[str] = None
    assignee: Optional[str] = None
    labels: Optional[List[str]] = None
    affected_feature: Optional[str] = None
    reproduction_steps: Optional[List[str]] = None
    related_tickets: Optional[List[str]] = None
    status: Optional[str] = None
    resolution: Optional[str] = None


class TicketResponse(TicketBase):
    id: str
    status: str
    assignee: Optional[str]
    resolution: Optional[str]
    resolved_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TicketStatusUpdate(BaseModel):
    status: str
    resolution: Optional[str] = None
    assignee: Optional[str] = None
