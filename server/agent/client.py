"""Stateful Claude Agent SDK client wrapper."""

import os
from typing import AsyncGenerator, Optional

from dotenv import load_dotenv

from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    AssistantMessage,
    TextBlock,
    ResultMessage,
    ClaudeSDKError,
)

from .memory import AgentMemory

# Load environment variables
load_dotenv(override=True)


class AgentClient:
    """
    Stateful agent client that wraps Claude Agent SDK.

    Unlike the stateless query() function, this client:
    - Maintains session state
    - Can resume previous sessions
    - Tracks costs and usage
    - Integrates with memory for persistence
    """

    def __init__(
        self,
        skills_dir: Optional[str] = None,
        max_turns: int = 20,
        max_budget_usd: float = 5.0
    ):
        self.skills_dir = skills_dir or os.getenv("SKILLS_DIR", "/app")
        self.max_turns = max_turns
        self.max_budget_usd = max_budget_usd
        self.memory = AgentMemory()

    def _get_options(self, claude_session_id: Optional[str] = None) -> ClaudeAgentOptions:
        """Build ClaudeAgentOptions with skills and settings.

        Args:
            claude_session_id: Optional CLAUDE session ID (from SDK) to resume.
                              NOT our database session ID.
        """
        options = ClaudeAgentOptions(
            cwd=self.skills_dir,
            setting_sources=["project"],  # Load skills from .claude/skills/
            permission_mode="bypassPermissions",
            max_turns=self.max_turns,
            max_budget_usd=self.max_budget_usd,
            allowed_tools=["Read", "Glob", "Grep", "Write", "Edit", "WebFetch"],
        )

        # Only resume if we have a valid Claude SDK session ID
        # NOTE: For MVP, we create new SDK sessions each time
        # TODO: Store and retrieve Claude session IDs for true resume
        # if claude_session_id and claude_session_id.startswith("claude-"):
        #     options.resume = claude_session_id

        return options

    async def chat(
        self,
        message: str,
        session_id: Optional[str] = None
    ) -> AsyncGenerator[dict, None]:
        """
        Send a message and stream responses.

        Args:
            message: User message
            session_id: Optional session ID to resume

        Yields:
            Dict with response chunks and metadata
        """
        # Create or resume session
        if not session_id:
            session_id = self.memory.create_session(metadata={"type": "chat"})
        else:
            # Verify session exists
            existing = self.memory.get_session(session_id)
            if not existing:
                session_id = self.memory.create_session(metadata={"type": "chat"})

        options = self._get_options()  # Don't pass DB session_id to SDK

        content_parts = []
        total_cost = 0.0
        duration_ms = 0

        try:
            async with ClaudeSDKClient(options=options) as client:
                # Send the query
                await client.query(message)

                # Receive and process response
                async for msg in client.receive_response():
                    if isinstance(msg, AssistantMessage):
                        for block in msg.content:
                            if isinstance(block, TextBlock):
                                content_parts.append(block.text)
                                yield {
                                    "type": "text",
                                    "content": block.text,
                                    "session_id": session_id
                                }

                    elif isinstance(msg, ResultMessage):
                        total_cost = msg.total_cost_usd or 0
                        duration_ms = msg.duration_ms or 0

                        yield {
                            "type": "result",
                            "session_id": session_id,
                            "is_error": msg.is_error,
                            "cost_usd": total_cost,
                            "duration_ms": duration_ms
                        }

            # Update session summary (first 200 chars of response)
            full_content = "".join(content_parts)
            if full_content:
                summary = full_content[:200] + "..." if len(full_content) > 200 else full_content
                self.memory.update_session(session_id, summary=summary)

        except ClaudeSDKError as e:
            yield {
                "type": "error",
                "session_id": session_id,
                "error": str(e)
            }

    async def chat_sync(
        self,
        message: str,
        session_id: Optional[str] = None
    ) -> dict:
        """
        Send a message and get complete response (non-streaming).

        Args:
            message: User message
            session_id: Optional session ID to resume

        Returns:
            Dict with full response and metadata
        """
        content_parts = []
        result_data = {}
        final_session_id = session_id
        received_any = False

        async for chunk in self.chat(message, session_id):
            received_any = True
            if chunk["type"] == "text":
                content_parts.append(chunk["content"])
                final_session_id = chunk.get("session_id") or final_session_id
            elif chunk["type"] == "result":
                result_data = chunk
                final_session_id = chunk.get("session_id") or final_session_id
            elif chunk["type"] == "error":
                return {
                    "content": "",
                    "session_id": chunk.get("session_id") or "error-session",
                    "error": chunk["error"],
                    "metadata": {"is_error": True}
                }

        # If no chunks received, create a session for tracking
        if not final_session_id:
            final_session_id = self.memory.create_session(metadata={"type": "chat", "note": "fallback"})

        return {
            "content": "".join(content_parts),
            "session_id": final_session_id,
            "metadata": {
                "is_error": result_data.get("is_error", False),
                "cost_usd": result_data.get("cost_usd", 0),
                "duration_ms": result_data.get("duration_ms", 0)
            }
        }

    async def run_task(
        self,
        goal: str,
        task_id: Optional[str] = None,
        webhook_url: Optional[str] = None
    ) -> dict:
        """
        Run an autonomous task to completion.

        Args:
            goal: The goal for the agent to achieve
            task_id: Optional existing task ID
            webhook_url: Optional URL to call when complete

        Returns:
            Dict with task result
        """
        # Create session for this task
        session_id = self.memory.create_session(metadata={
            "type": "task",
            "goal": goal
        })

        # Create or update task record
        if not task_id:
            task_id = self.memory.create_task(
                goal=goal,
                session_id=session_id,
                webhook_url=webhook_url
            )
        else:
            self.memory.update_task(task_id, status="in_progress")

        # Build prompt with goal context
        prompt = f"""You are an autonomous marketing agent. Your goal is:

{goal}

Work toward this goal step by step. Use the available skills (brand-voice, linkedin-viral, direct-response-copy, seo-content, geo-content) as appropriate.

When you have completed the goal or made significant progress, summarize what you accomplished."""

        # Run the task
        result = await self.chat_sync(prompt, session_id)

        # Update task with result
        if result.get("error"):
            self.memory.update_task(
                task_id,
                status="failed",
                error=result["error"],
                cost_usd=result.get("metadata", {}).get("cost_usd", 0)
            )
        else:
            self.memory.update_task(
                task_id,
                status="completed",
                progress="Goal completed",
                result={"content": result["content"][:1000]},  # Truncate for storage
                cost_usd=result.get("metadata", {}).get("cost_usd", 0)
            )

        # TODO: Call webhook if provided
        # if webhook_url:
        #     await call_webhook(webhook_url, result)

        return {
            "task_id": task_id,
            "session_id": session_id,
            "status": "failed" if result.get("error") else "completed",
            "content": result.get("content", ""),
            "error": result.get("error"),
            "metadata": result.get("metadata", {})
        }
