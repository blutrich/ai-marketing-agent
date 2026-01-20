"""Pydantic request models."""

from typing import Optional
from pydantic import BaseModel, Field, HttpUrl


class ChatRequest(BaseModel):
    """Request model for /agent/chat endpoint."""

    message: str = Field(
        ...,
        description="The message to send to the agent",
        examples=["Plan this week's LinkedIn content"]
    )
    session_id: Optional[str] = Field(
        default=None,
        description="Optional session ID to resume a previous conversation"
    )


class TaskRequest(BaseModel):
    """Request model for /agent/task endpoint."""

    goal: str = Field(
        ...,
        description="The goal for the agent to achieve autonomously",
        examples=["Create 5 LinkedIn posts about AI ROI"]
    )
    webhook_url: Optional[HttpUrl] = Field(
        default=None,
        description="Optional URL to call when task completes"
    )
    max_turns: Optional[int] = Field(
        default=None,
        description="Optional max turns override"
    )
    max_budget_usd: Optional[float] = Field(
        default=None,
        description="Optional max budget override"
    )


class ContentRequest(BaseModel):
    """Request model for /generate-content endpoint (stateless)."""

    prompt: str = Field(
        ...,
        description="The prompt describing what content to generate",
        examples=["Write a LinkedIn post about AI consulting services"]
    )
    content_type: str = Field(
        default="general",
        description="Type of content to generate",
        examples=["linkedin", "email", "seo", "direct-response"]
    )
    additional_context: Optional[str] = Field(
        default=None,
        description="Optional additional context or requirements"
    )
