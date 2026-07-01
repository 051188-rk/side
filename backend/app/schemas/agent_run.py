from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class AgentRunBase(BaseModel):
    agent_name: str
    input_data: Dict[str, Any]
    feedback_id: Optional[str] = None
    ticket_id: Optional[str] = None


class AgentRunCreate(AgentRunBase):
    pass


class AgentRunResponse(AgentRunBase):
    id: str
    status: str
    output_data: Optional[Dict[str, Any]]
    error: Optional[str]
    duration_ms: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
