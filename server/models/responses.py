"""Pydantic response models."""

from typing import Optional, List
from pydantic import BaseModel


class ChatMetadata(BaseModel):
    """Metadata about a chat response."""

    is_error: bool = False
    cost_usd: Optional[float] = None
    duration_ms: Optional[int] = None


class ChatResponse(BaseModel):
    """Response model for /agent/chat endpoint."""

    content: str
    session_id: str
    metadata: ChatMetadata


class TaskResponse(BaseModel):
    """Response model for /agent/task endpoint."""

    task_id: str
    session_id: str
    status: str
    message: str = "Task started"


class TaskStatusResponse(BaseModel):
    """Response model for /agent/status endpoint."""

    task_id: str
    status: str
    progress: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    cost_usd: Optional[float] = None
    error: Optional[str] = None
    result: Optional[dict] = None


class SessionSummary(BaseModel):
    """Summary of a session."""

    session_id: str
    created_at: str
    summary: Optional[str] = None
    tags: Optional[List[str]] = None


class ContentSummary(BaseModel):
    """Summary of content created."""

    id: str
    created_at: str
    content_type: str
    platform: Optional[str] = None
    title: Optional[str] = None
    preview: str  # First 100 chars


class HistoryResponse(BaseModel):
    """Response model for /agent/history endpoint."""

    sessions: List[SessionSummary]
    content: List[ContentSummary]
    stats: dict


class ContentMetadata(BaseModel):
    """Metadata about content generation."""

    is_error: bool = False
    cost_usd: Optional[float] = None
    duration_ms: Optional[int] = None
    content_type: str = "general"


class ContentResponse(BaseModel):
    """Response model for /generate-content endpoint."""

    content: str
    metadata: ContentMetadata


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    skills_loaded: List[str]
    skills_directory: str
    database_connected: bool = False
