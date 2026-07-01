"""
Feedback data models

This module contains Pydantic models for feedback-related data structures.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class FeedbackModel(BaseModel):
    """Core feedback model."""
    id: Optional[str] = None
    source: str
    content: str
    customer_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    status: str = "pending"
    processed: bool = False
    ticket_id: Optional[str] = None
    duplicate_cluster_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class FeedbackAnalysisModel(BaseModel):
    """Model for feedback analysis results."""
    feedback_id: str
    cleaned_content: Optional[str] = None
    is_spam: bool = False
    language: Optional[str] = None
    category: Optional[str] = None
    severity: Optional[str] = None
    sentiment: Optional[str] = None
    is_duplicate: bool = False
    cluster_id: Optional[str] = None
    priority_score: Optional[float] = None
    analysis_timestamp: datetime = Field(default_factory=datetime.utcnow)


class FeedbackSourceModel(BaseModel):
    """Model for feedback source configuration."""
    source_type: str
    enabled: bool = True
    config: Dict[str, Any] = Field(default_factory=dict)
    last_sync: Optional[datetime] = None
    sync_frequency_minutes: int = 5
