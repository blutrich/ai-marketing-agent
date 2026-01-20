"""Agent memory operations using Supabase."""

import logging
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from db.supabase import get_supabase_client

logger = logging.getLogger(__name__)


class AgentMemory:
    """Manages agent memory persistence in Supabase."""

    def __init__(self):
        self.client = get_supabase_client()

    # ==================== Sessions ====================

    def create_session(self, metadata: Optional[dict] = None) -> str:
        """Create a new session and return session_id."""
        session_id = f"session-{uuid.uuid4().hex[:12]}"

        try:
            self.client.table("sessions").insert({
                "session_id": session_id,
                "metadata": metadata or {}
            }).execute()
        except Exception as e:
            logger.error(f"Failed to create session: {e}")
            raise RuntimeError(f"Database error: {e}")

        return session_id

    def get_session(self, session_id: str) -> Optional[dict]:
        """Get session by ID."""
        try:
            result = self.client.table("sessions").select("*").eq(
                "session_id", session_id
            ).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Failed to get session {session_id}: {e}")
            raise RuntimeError(f"Database error: {e}")

    def update_session(
        self,
        session_id: str,
        summary: Optional[str] = None,
        tags: Optional[list] = None,
        metadata: Optional[dict] = None
    ) -> None:
        """Update session with summary, tags, or metadata."""
        update_data = {}
        if summary is not None:
            update_data["summary"] = summary
        if tags is not None:
            update_data["tags"] = tags
        if metadata is not None:
            update_data["metadata"] = metadata

        if update_data:
            try:
                self.client.table("sessions").update(update_data).eq(
                    "session_id", session_id
                ).execute()
            except Exception as e:
                logger.error(f"Failed to update session {session_id}: {e}")
                raise RuntimeError(f"Database error: {e}")

    def list_sessions(self, limit: int = 20) -> list:
        """List recent sessions."""
        try:
            result = self.client.table("sessions").select("*").order(
                "created_at", desc=True
            ).limit(limit).execute()
            return result.data
        except Exception as e:
            logger.error(f"Failed to list sessions: {e}")
            raise RuntimeError(f"Database error: {e}")

    # ==================== Messages ====================

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
        metadata: Optional[dict] = None
    ) -> str:
        """Add a message to conversation history."""
        message_id = str(uuid.uuid4())

        try:
            self.client.table("messages").insert({
                "id": message_id,
                "session_id": session_id,
                "role": role,
                "content": content,
                "metadata": metadata or {}
            }).execute()
        except Exception as e:
            logger.error(f"Failed to add message: {e}")
            raise RuntimeError(f"Database error: {e}")

        return message_id

    def get_messages(self, session_id: str, limit: int = 50) -> list:
        """Get conversation history for a session."""
        try:
            result = self.client.table("messages").select("*").eq(
                "session_id", session_id
            ).order("created_at", desc=False).limit(limit).execute()
            return result.data
        except Exception as e:
            logger.error(f"Failed to get messages for {session_id}: {e}")
            raise RuntimeError(f"Database error: {e}")

    def get_conversation_context(self, session_id: str, limit: int = 20) -> str:
        """Get formatted conversation history as context string."""
        messages = self.get_messages(session_id, limit)
        if not messages:
            return ""

        context_parts = ["Previous conversation:"]
        for msg in messages:
            role = "User" if msg["role"] == "user" else "Assistant"
            # Truncate long messages for context
            content = msg["content"][:500] + "..." if len(msg["content"]) > 500 else msg["content"]
            context_parts.append(f"{role}: {content}")

        return "\n\n".join(context_parts)

    # ==================== Content Log ====================

    def log_content(
        self,
        content: str,
        content_type: str,
        session_id: Optional[str] = None,
        platform: Optional[str] = None,
        title: Optional[str] = None,
        metadata: Optional[dict] = None
    ) -> str:
        """Log content created by the agent."""
        content_id = str(uuid.uuid4())

        try:
            self.client.table("content_log").insert({
                "id": content_id,
                "session_id": session_id,
                "content_type": content_type,
                "platform": platform,
                "title": title,
                "content": content,
                "metadata": metadata or {}
            }).execute()
        except Exception as e:
            logger.error(f"Failed to log content: {e}")
            raise RuntimeError(f"Database error: {e}")

        return content_id

    def get_recent_content(self, days: int = 30, limit: int = 50) -> list:
        """Get content created in the last N days."""
        since = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()

        try:
            result = self.client.table("content_log").select("*").gte(
                "created_at", since
            ).order("created_at", desc=True).limit(limit).execute()
            return result.data
        except Exception as e:
            logger.error(f"Failed to get recent content: {e}")
            raise RuntimeError(f"Database error: {e}")

    def get_content_by_type(self, content_type: str, limit: int = 20) -> list:
        """Get content by type (linkedin, email, etc.)."""
        try:
            result = self.client.table("content_log").select("*").eq(
                "content_type", content_type
            ).order("created_at", desc=True).limit(limit).execute()
            return result.data
        except Exception as e:
            logger.error(f"Failed to get content by type {content_type}: {e}")
            raise RuntimeError(f"Database error: {e}")

    def search_content(self, query: str, limit: int = 20) -> list:
        """Search content by text (basic ILIKE search)."""
        try:
            result = self.client.table("content_log").select("*").ilike(
                "content", f"%{query}%"
            ).order("created_at", desc=True).limit(limit).execute()
            return result.data
        except Exception as e:
            logger.error(f"Failed to search content: {e}")
            raise RuntimeError(f"Database error: {e}")

    def update_content_performance(
        self,
        content_id: str,
        performance: dict
    ) -> None:
        """Update content with performance metrics."""
        try:
            self.client.table("content_log").update({
                "performance": performance
            }).eq("id", content_id).execute()
        except Exception as e:
            logger.error(f"Failed to update content performance: {e}")
            raise RuntimeError(f"Database error: {e}")

    # ==================== Preferences ====================

    def get_preference(self, key: str) -> Optional[dict]:
        """Get a preference by key."""
        try:
            result = self.client.table("preferences").select("value").eq(
                "key", key
            ).execute()
            return result.data[0]["value"] if result.data else None
        except Exception as e:
            logger.error(f"Failed to get preference {key}: {e}")
            raise RuntimeError(f"Database error: {e}")

    def set_preference(self, key: str, value: dict) -> None:
        """Set a preference (upsert)."""
        try:
            self.client.table("preferences").upsert({
                "key": key,
                "value": value
            }, on_conflict="key").execute()
        except Exception as e:
            logger.error(f"Failed to set preference {key}: {e}")
            raise RuntimeError(f"Database error: {e}")

    def get_all_preferences(self) -> dict:
        """Get all preferences as a dictionary."""
        try:
            result = self.client.table("preferences").select("*").execute()
            return {row["key"]: row["value"] for row in result.data}
        except Exception as e:
            logger.error(f"Failed to get all preferences: {e}")
            raise RuntimeError(f"Database error: {e}")

    # ==================== Tasks ====================

    def create_task(
        self,
        goal: str,
        session_id: Optional[str] = None,
        webhook_url: Optional[str] = None
    ) -> str:
        """Create a new autonomous task."""
        task_id = f"task-{uuid.uuid4().hex[:12]}"

        try:
            self.client.table("tasks").insert({
                "task_id": task_id,
                "session_id": session_id,
                "goal": goal,
                "status": "pending",
                "webhook_url": webhook_url
            }).execute()
        except Exception as e:
            logger.error(f"Failed to create task: {e}")
            raise RuntimeError(f"Database error: {e}")

        return task_id

    def update_task(
        self,
        task_id: str,
        status: Optional[str] = None,
        progress: Optional[str] = None,
        result: Optional[dict] = None,
        error: Optional[str] = None,
        cost_usd: Optional[float] = None
    ) -> None:
        """Update task status and progress."""
        update_data = {}

        if status is not None:
            update_data["status"] = status
            if status == "in_progress" and "started_at" not in update_data:
                update_data["started_at"] = datetime.now(timezone.utc).isoformat()
            elif status in ("completed", "failed"):
                update_data["completed_at"] = datetime.now(timezone.utc).isoformat()

        if progress is not None:
            update_data["progress"] = progress
        if result is not None:
            update_data["result"] = result
        if error is not None:
            update_data["error"] = error
        if cost_usd is not None:
            update_data["cost_usd"] = cost_usd

        if update_data:
            try:
                self.client.table("tasks").update(update_data).eq(
                    "task_id", task_id
                ).execute()
            except Exception as e:
                logger.error(f"Failed to update task {task_id}: {e}")
                raise RuntimeError(f"Database error: {e}")

    def get_task(self, task_id: str) -> Optional[dict]:
        """Get task by ID."""
        try:
            result = self.client.table("tasks").select("*").eq(
                "task_id", task_id
            ).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Failed to get task {task_id}: {e}")
            raise RuntimeError(f"Database error: {e}")

    def list_tasks(self, status: Optional[str] = None, limit: int = 20) -> list:
        """List tasks, optionally filtered by status."""
        try:
            query = self.client.table("tasks").select("*")

            if status:
                query = query.eq("status", status)

            result = query.order("started_at", desc=True).limit(limit).execute()
            return result.data
        except Exception as e:
            logger.error(f"Failed to list tasks: {e}")
            raise RuntimeError(f"Database error: {e}")

    # ==================== Aggregations ====================

    def get_stats(self) -> dict:
        """Get overall agent statistics."""
        try:
            sessions = self.client.table("sessions").select(
                "id", count="exact"
            ).execute()

            content = self.client.table("content_log").select(
                "id", count="exact"
            ).execute()

            tasks = self.client.table("tasks").select(
                "id", count="exact"
            ).execute()

            return {
                "total_sessions": sessions.count or 0,
                "total_content": content.count or 0,
                "total_tasks": tasks.count or 0
            }
        except Exception as e:
            logger.error(f"Failed to get stats: {e}")
            raise RuntimeError(f"Database error: {e}")
