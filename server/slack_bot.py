"""Slack Bot for Marketing Agent.

Simple Slack integration that connects to the existing agent API.
Uses Socket Mode for easy setup (no public URL needed).
"""

import os
import logging
import httpx
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Slack app setup
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Agent API URL (Railway deployment or local)
AGENT_API_URL = os.environ.get(
    "AGENT_API_URL",
    "https://ai-marketing-agent-production-60c7.up.railway.app"
)

# Store user sessions: slack_user_id -> agent_session_id
user_sessions: dict[str, str] = {}


async def call_agent(user_id: str, message: str) -> str:
    """Call the marketing agent API."""
    session_id = user_sessions.get(user_id)

    payload = {"message": message}
    if session_id:
        payload["session_id"] = session_id

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{AGENT_API_URL}/agent/chat",
            json=payload
        )
        response.raise_for_status()
        data = response.json()

        # Store session for continuity
        if "session_id" in data:
            user_sessions[user_id] = data["session_id"]

        return data.get("content", "Sorry, I couldn't generate a response.")


@app.event("app_mention")
def handle_mention(event, say, client):
    """Handle @MarketingBot mentions in channels."""
    user_id = event["user"]
    text = event["text"]
    thread_ts = event.get("thread_ts") or event["ts"]

    # Remove the bot mention from the message
    # Format: <@BOT_ID> message
    message = text.split(">", 1)[-1].strip() if ">" in text else text

    if not message:
        say("Hi! How can I help with your marketing today?", thread_ts=thread_ts)
        return

    # Show typing indicator
    say("Thinking...", thread_ts=thread_ts)

    try:
        import asyncio
        response = asyncio.run(call_agent(user_id, message))
        say(response, thread_ts=thread_ts)
    except Exception as e:
        logger.error(f"Agent error: {e}")
        say(f"Sorry, something went wrong. Please try again.", thread_ts=thread_ts)


@app.event("message")
def handle_dm(event, say, client):
    """Handle direct messages to the bot."""
    # Ignore bot messages and channel messages
    if event.get("bot_id") or event.get("channel_type") != "im":
        return

    user_id = event["user"]
    message = event["text"]

    if not message:
        return

    try:
        import asyncio
        response = asyncio.run(call_agent(user_id, message))
        say(response)
    except Exception as e:
        logger.error(f"Agent error: {e}")
        say("Sorry, something went wrong. Please try again.")


@app.command("/marketing")
def handle_slash_command(ack, respond, command):
    """Handle /marketing slash command."""
    ack()

    user_id = command["user_id"]
    message = command["text"]

    if not message:
        respond("Usage: `/marketing <your request>`\n\nExample: `/marketing Write a LinkedIn post about AI consulting`")
        return

    respond("Thinking...")

    try:
        import asyncio
        response = asyncio.run(call_agent(user_id, message))
        respond(response)
    except Exception as e:
        logger.error(f"Agent error: {e}")
        respond("Sorry, something went wrong. Please try again.")


@app.command("/clear")
def handle_clear(ack, respond, command):
    """Clear conversation history for the user."""
    ack()
    user_id = command["user_id"]

    if user_id in user_sessions:
        del user_sessions[user_id]
        respond("Conversation cleared! I've forgotten our previous chat.")
    else:
        respond("No conversation to clear.")


if __name__ == "__main__":
    # Socket Mode uses WebSocket - no public URL needed
    handler = SocketModeHandler(
        app,
        os.environ.get("SLACK_APP_TOKEN")
    )
    logger.info("Starting Slack bot in Socket Mode...")
    handler.start()
