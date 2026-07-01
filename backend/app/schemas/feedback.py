from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class FeedbackBase(BaseModel):
    source: str
    content: str
    customer_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class FeedbackCreate(FeedbackBase):
    pass


class FeedbackUpdate(BaseModel):
    content: Optional[str] = None
    status: Optional[str] = None
    processed: Optional[bool] = None
    ticket_id: Optional[str] = None
    duplicate_cluster_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class FeedbackResponse(FeedbackBase):
    id: str
    status: str
    processed: bool
    ticket_id: Optional[str]
    duplicate_cluster_id: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class FeedbackClassification(BaseModel):
    category: str
    confidence: float


class FeedbackSentiment(BaseModel):
    sentiment: str
    confidence: float


class FeedbackSeverity(BaseModel):
    severity: str
    confidence: float
