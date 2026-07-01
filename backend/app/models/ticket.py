"""
Ticket data models

This module contains Pydantic models for ticket-related data structures.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class TicketModel(BaseModel):
    """Core ticket model."""
    id: Optional[str] = None
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
    status: str = "open"
    assignee: Optional[str] = None
    resolution: Optional[str] = None
    resolved_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class TicketWorkflowModel(BaseModel):
    """Model for ticket workflow state."""
    ticket_id: str
    current_status: str
    previous_status: Optional[str] = None
    assigned_to: Optional[str] = None
    time_in_status: int = 0
    sla_deadline: Optional[datetime] = None
    escalation_level: int = 0


class TicketMetricsModel(BaseModel):
    """Model for ticket metrics."""
    ticket_id: str
    total_time_to_resolution: Optional[int] = None
    agent_response_time: Optional[int] = None
    customer_satisfaction: Optional[int] = None
    resolution_count: int = 0
    reopen_count: int = 0
