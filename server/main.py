"""
AI Marketing Agent Server

This server provides both:
1. Stateless webhook endpoints (existing /generate-content)
2. Stateful agent endpoints (new /agent/*)

Endpoints:
- POST /generate-content: Stateless content generation
- POST /agent/chat: Stateful conversation with agent
- POST /agent/task: Assign autonomous task
- GET /agent/status/{task_id}: Check task status
- GET /agent/history: List sessions and content
- GET /health: Health check for Railway
"""

import os
import sys
from contextlib import asynccontextmanager
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    AssistantMessage,
    TextBlock,
    ResultMessage,
    ClaudeSDKError,
    CLINotFoundError,
    CLIConnectionError,
    ProcessError,
    CLIJSONDecodeError,
)

# Load environment variables (override=True to use .env over shell vars)
load_dotenv(override=True)

# Add server directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent import AgentClient, AgentMemory
from models import (
    ChatRequest,
    TaskRequest,
    ChatResponse,
    TaskResponse,
    TaskStatusResponse,
    HistoryResponse,
    ContentResponse,
    HealthResponse,
    ContentRequest,
    ChatMetadata,
    ContentMetadata,
    SessionSummary,
    ContentSummary,
)

# Configuration
SKILLS_DIR = os.getenv("SKILLS_DIR", "/app")
MAX_TURNS = int(os.getenv("MAX_TURNS", "20"))
MAX_BUDGET_USD = float(os.getenv("MAX_BUDGET_USD", "5.0"))

# Global instances
agent_client: Optional[AgentClient] = None
agent_memory: Optional[AgentMemory] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    global agent_client, agent_memory

    # Verify skills directory exists
    skills_path = os.path.join(SKILLS_DIR, ".claude", "skills")
    if os.path.exists(skills_path):
        skills = os.listdir(skills_path)
        print(f"Skills loaded from {skills_path}: {skills}")
    else:
        print(f"Warning: Skills directory not found at {skills_path}")

    # Initialize agent client and memory
    try:
        agent_client = AgentClient(
            skills_dir=SKILLS_DIR,
            max_turns=MAX_TURNS,
            max_budget_usd=MAX_BUDGET_USD
        )
        agent_memory = AgentMemory()
        print("Agent client and memory initialized")
    except Exception as e:
        print(f"Warning: Could not initialize agent: {e}")
        print("Stateless endpoints will still work")

    yield

    # Cleanup
    agent_client = None
    agent_memory = None


app = FastAPI(
    title="AI Marketing Agent",
    description="Stateful AI agent for marketing content generation with memory",
    version="2.0.0",
    lifespan=lifespan,
)

# CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== Helper Functions ====================

def build_prompt(request: ContentRequest) -> str:
    """Build the full prompt with content type hints for skill activation."""
    content_type_hints = {
        "linkedin": "Use the linkedin-viral skill to format this content for LinkedIn with hooks and engagement patterns.",
        "email": "Use the direct-response-copy skill with THE SLIDE framework for this email content.",
        "seo": "Use the seo-content skill to optimize this content for search engines.",
        "geo": "Use the geo-content skill to optimize this content for AI citation and LLM discovery.",
        "direct-response": "Use the direct-response-copy skill with THE SLIDE framework.",
        "landing-page": "Use the landing-page-architecture skill with the 8-Section Framework: HERO, SUCCESS, PROBLEM-AGITATE, VALUE STACK, SOCIAL PROOF, TRANSFORMATION, SECONDARY CTA, FOOTER. Each section has ONE job.",
        "general": "Apply the brand-voice skill to ensure consistent tone and messaging.",
    }

    hint = content_type_hints.get(request.content_type, content_type_hints["general"])

    prompt_parts = [
        f"Content Type: {request.content_type}",
        f"Skill Hint: {hint}",
        "",
        f"Request: {request.prompt}",
    ]

    if request.additional_context:
        prompt_parts.insert(3, f"Additional Context: {request.additional_context}")

    return "\n".join(prompt_parts)


# ==================== Health & Info Endpoints ====================

@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {
        "service": "AI Marketing Agent",
        "version": "2.0.0",
        "endpoints": {
            "stateless": {
                "health": "GET /health",
                "generate": "POST /generate-content"
            },
            "stateful": {
                "chat": "POST /agent/chat",
                "task": "POST /agent/task",
                "status": "GET /agent/status/{task_id}",
                "history": "GET /agent/history"
            }
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for Railway and monitoring."""
    skills_path = os.path.join(SKILLS_DIR, ".claude", "skills")
    skills = []
    db_connected = False

    if os.path.exists(skills_path):
        skills = [d for d in os.listdir(skills_path)
                  if os.path.isdir(os.path.join(skills_path, d))]

    # Check database connection
    if agent_memory:
        try:
            agent_memory.get_stats()
            db_connected = True
        except Exception:
            db_connected = False

    return {
        "status": "ok",
        "skills_loaded": skills,
        "skills_directory": skills_path,
        "database_connected": db_connected,
        "agent_ready": agent_client is not None
    }


# ==================== Stateless Endpoints ====================

@app.post("/generate-content")
async def generate_content(request: ContentRequest):
    """
    Generate marketing content (stateless).

    This is the original webhook endpoint - no memory, no session.
    Good for simple integrations that don't need state.
    """
    full_prompt = build_prompt(request)

    options = ClaudeAgentOptions(
        cwd=SKILLS_DIR,
        setting_sources=["project"],
        permission_mode="bypassPermissions",
        max_turns=MAX_TURNS,
        max_budget_usd=MAX_BUDGET_USD,
        allowed_tools=["Read", "Glob", "Grep"],
    )

    content_parts = []
    metadata = ContentMetadata(content_type=request.content_type)

    try:
        async for message in query(prompt=full_prompt, options=options):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        content_parts.append(block.text)
            elif isinstance(message, ResultMessage):
                metadata.is_error = message.is_error
                metadata.cost_usd = message.total_cost_usd
                metadata.duration_ms = message.duration_ms

        content = "".join(content_parts)

        if not content:
            raise HTTPException(
                status_code=500,
                detail="No content generated. Check that skills are properly loaded."
            )

        return ContentResponse(content=content, metadata=metadata)

    except CLINotFoundError:
        raise HTTPException(500, "Claude Code CLI not installed")
    except CLIConnectionError as e:
        raise HTTPException(500, f"Connection error: {e}")
    except ProcessError as e:
        raise HTTPException(500, f"Process failed: {e.stderr or e}")
    except CLIJSONDecodeError as e:
        raise HTTPException(500, f"Parse error: {e}")
    except ClaudeSDKError as e:
        raise HTTPException(500, f"SDK error: {e}")


# ==================== Stateful Agent Endpoints ====================

@app.post("/agent/chat")
async def agent_chat(request: ChatRequest):
    """
    Stateful conversation with the agent.

    The agent remembers previous messages in the session.
    Pass session_id to continue a previous conversation.
    """
    if not agent_client:
        raise HTTPException(503, "Agent not initialized. Check database connection.")

    try:
        result = await agent_client.chat_sync(
            message=request.message,
            session_id=request.session_id
        )

        if result.get("error"):
            raise HTTPException(500, result["error"])

        return ChatResponse(
            content=result["content"],
            session_id=result["session_id"],
            metadata=ChatMetadata(
                is_error=result["metadata"].get("is_error", False),
                cost_usd=result["metadata"].get("cost_usd"),
                duration_ms=result["metadata"].get("duration_ms")
            )
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Chat failed: {e}")


@app.post("/agent/task")
async def agent_task(request: TaskRequest):
    """
    Assign an autonomous task to the agent.

    The agent will work toward the goal and track progress.
    Poll /agent/status/{task_id} to check progress.
    """
    if not agent_client:
        raise HTTPException(503, "Agent not initialized. Check database connection.")

    if not agent_memory:
        raise HTTPException(503, "Memory not initialized. Check database connection.")

    try:
        # Create task record first
        session_id = agent_memory.create_session(metadata={
            "type": "task",
            "goal": request.goal
        })

        task_id = agent_memory.create_task(
            goal=request.goal,
            session_id=session_id,
            webhook_url=request.webhook_url
        )

        agent_memory.update_task(task_id, status="in_progress")

        # For MVP, run task synchronously (blocking)
        # TODO: Run in background for true async
        result = await agent_client.run_task(
            goal=request.goal,
            task_id=task_id,
            webhook_url=request.webhook_url
        )

        return TaskResponse(
            task_id=task_id,
            session_id=session_id,
            status=result["status"],
            message=f"Task {result['status']}"
        )

    except Exception as e:
        raise HTTPException(500, f"Task creation failed: {e}")


@app.get("/agent/status/{task_id}")
async def agent_status(task_id: str):
    """Get the status of an autonomous task."""
    if not agent_memory:
        raise HTTPException(503, "Memory not initialized")

    task = agent_memory.get_task(task_id)

    if not task:
        raise HTTPException(404, f"Task {task_id} not found")

    return TaskStatusResponse(
        task_id=task["task_id"],
        status=task["status"],
        progress=task.get("progress"),
        started_at=task.get("started_at"),
        completed_at=task.get("completed_at"),
        cost_usd=float(task["cost_usd"]) if task.get("cost_usd") else None,
        error=task.get("error"),
        result=task.get("result")
    )


@app.get("/agent/history")
async def agent_history(limit: int = 20):
    """
    Get agent history: recent sessions and content created.

    Use this to see what the agent has been working on.
    """
    if not agent_memory:
        raise HTTPException(503, "Memory not initialized")

    try:
        sessions = agent_memory.list_sessions(limit=limit)
        content = agent_memory.get_recent_content(days=90, limit=limit)
        stats = agent_memory.get_stats()

        return HistoryResponse(
            sessions=[
                SessionSummary(
                    session_id=s["session_id"],
                    created_at=s["created_at"],
                    summary=s.get("summary"),
                    tags=s.get("tags")
                )
                for s in sessions
            ],
            content=[
                ContentSummary(
                    id=c["id"],
                    created_at=c["created_at"],
                    content_type=c["content_type"],
                    platform=c.get("platform"),
                    title=c.get("title"),
                    preview=c["content"][:100] + "..." if len(c["content"]) > 100 else c["content"]
                )
                for c in content
            ],
            stats=stats
        )

    except Exception as e:
        raise HTTPException(500, f"Failed to fetch history: {e}")


# ==================== Main ====================

if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
