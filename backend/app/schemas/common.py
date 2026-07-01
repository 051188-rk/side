from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Generic, TypeVar
from datetime import datetime


T = TypeVar('T')


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int


class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: datetime


class ErrorResponse(BaseModel):
    error: Dict[str, Any]


class SuccessResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None


class WebhookPayload(BaseModel):
    source: str
    event_type: str
    data: Dict[str, Any]
    timestamp: Optional[datetime] = None
    signature: Optional[str] = None


class AgentInput(BaseModel):
    feedback_id: Optional[str] = None
    ticket_id: Optional[str] = None
    content: Optional[str] = None
    context: Dict[str, Any] = Field(default_factory=dict)


class AgentOutput(BaseModel):
    success: bool
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    duration_ms: int
