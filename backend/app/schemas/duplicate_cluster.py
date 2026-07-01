from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class DuplicateClusterBase(BaseModel):
    representative_feedback_id: str
    similarity_threshold: float
    ticket_id: Optional[str] = None
    title: str
    description: str


class DuplicateClusterCreate(BaseModel):
    representative_feedback_id: str
    similarity_threshold: float
    feedback_ids: List[str]
    title: str
    description: str


class DuplicateClusterUpdate(BaseModel):
    ticket_id: Optional[str] = None
    status: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None


class DuplicateClusterResponse(DuplicateClusterBase):
    id: str
    feedback_ids: List[str]
    status: str
    count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
