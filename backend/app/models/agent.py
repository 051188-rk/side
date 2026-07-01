"""
Agent data models

This module contains Pydantic models for agent-related data structures.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class AgentRunModel(BaseModel):
    """Model for agent execution run."""
    id: Optional[str] = None
    agent_name: str
    input_data: Dict[str, Any]
    feedback_id: Optional[str] = None
    ticket_id: Optional[str] = None
    status: str = "running"
    output_data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    duration_ms: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class AgentConfigModel(BaseModel):
    """Model for agent configuration."""
    agent_name: str
    enabled: bool = True
    max_retries: int = 3
    timeout_seconds: int = 300
    fallback_enabled: bool = True
    custom_config: Dict[str, Any] = Field(default_factory=dict)


class AgentMetricsModel(BaseModel):
    """Model for agent performance metrics."""
    agent_name: str
    total_runs: int = 0
    successful_runs: int = 0
    failed_runs: int = 0
    average_duration_ms: float = 0.0
    last_run_time: Optional[datetime] = None
    error_rate: float = 0.0
