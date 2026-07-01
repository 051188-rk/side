"""
Event type definitions

This module defines all event types used throughout the application.
"""

from enum import Enum
from typing import Any, Dict
from pydantic import BaseModel, Field


class EventType(str, Enum):
    """All event types in the system."""
    
    # Feedback events
    FEEDBACK_CREATED = "feedback.created"
    FEEDBACK_PROCESSED = "feedback.processed"
    FEEDBACK_CLASSIFIED = "feedback.classified"
    
    # Ticket events
    TICKET_CREATED = "ticket.created"
    TICKET_UPDATED = "ticket.updated"
    TICKET_ASSIGNED = "ticket.assigned"
    TICKET_RESOLVED = "ticket.resolved"
    TICKET_CLOSED = "ticket.closed"
    
    # Agent events
    AGENT_STARTED = "agent.started"
    AGENT_COMPLETED = "agent.completed"
    AGENT_FAILED = "agent.failed"
    
    # User events
    USER_CREATED = "user.created"
    USER_LOGIN = "user.login"
    USER_LOGOUT = "user.logout"
    
    # Webhook events
    WEBHOOK_RECEIVED = "webhook.received"
    WEBHOOK_PROCESSED = "webhook.processed"
    WEBHOOK_FAILED = "webhook.failed"
    
    # Integration events
    INTEGRATION_CONNECTED = "integration.connected"
    INTEGRATION_DISCONNECTED = "integration.disconnected"
    INTEGRATION_ERROR = "integration.error"
    
    # Memory events
    MEMORY_STORED = "memory.stored"
    MEMORY_RETRIEVED = "memory.retrieved"
    
    # Insight events
    INSIGHT_GENERATED = "insight.generated"
    REPORT_CREATED = "report.created"


class BaseEvent(BaseModel):
    """Base event model."""
    event_type: EventType
    timestamp: float
    data: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class FeedbackCreatedEvent(BaseEvent):
    """Event emitted when feedback is created."""
    event_type: EventType = EventType.FEEDBACK_CREATED


class TicketCreatedEvent(BaseEvent):
    """Event emitted when a ticket is created."""
    event_type: EventType = EventType.TICKET_CREATED


class AgentCompletedEvent(BaseEvent):
    """Event emitted when an agent completes execution."""
    event_type: EventType = EventType.AGENT_COMPLETED
