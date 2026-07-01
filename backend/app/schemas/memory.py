from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class MemoryBase(BaseModel):
    memory_type: str
    content: str
    embedding: Optional[List[float]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    related_entities: List[str] = Field(default_factory=list)


class MemoryCreate(MemoryBase):
    pass


class MemoryUpdate(BaseModel):
    content: Optional[str] = None
    embedding: Optional[List[float]] = None
    metadata: Optional[Dict[str, Any]] = None
    related_entities: Optional[List[str]] = None


class MemoryResponse(MemoryBase):
    id: str
    access_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MemorySearch(BaseModel):
    query: str
    memory_type: Optional[str] = None
    limit: int = 10
