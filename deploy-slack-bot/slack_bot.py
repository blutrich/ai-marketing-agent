"""Slack Bot for Marketing Agent.

Simple Slack integration that connects to the existing agent API.
Uses Socket Mode for easy setup (no public URL needed).
Persists user sessions in Supabase.
"""

import os
import logging
import httpx
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
from supabase import create_client, Client

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

# Supabase client for persisting user sessions
supabase: Client = None
try:
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_KEY")
    if supabase_url and supabase_key:
        supabase = create_client(supabase_url, supabase_key)
        logger.info("Supabase connected for session persistence")
    else:
        logger.warning("Supabase not configured - sessions won't persist across restarts")
except Exception as e:
    logger.error(f"Failed to connect to Supabase: {e}")

# Fallback in-memory storage if Supabase not available
memory_sessions: dict[str, str] = {}


def get_user_session(slack_user_id: str) -> str | None:
    """Get session ID for a Slack user."""
    if supabase:
        try:
            result = supabase.table("slack_users").select("session_id").eq(
                "slack_user_id", slack_user_id
            ).execute()
            if result.data and result.data[0].get("session_id"):
                return result.data[0]["session_id"]
        except Exception as e:
            logger.error(f"Failed to get user session: {e}")
    return memory_sessions.get(slack_user_id)


def save_user_session(slack_user_id: str, session_id: str, username: str = None):
    """Save session ID for a Slack user."""
    memory_sessions[slack_user_id] = session_id

    if supabase:
        try:
            supabase.table("slack_users").upsert({
                "slack_user_id": slack_user_id,
                "session_id": session_id,
                "slack_username": username,
                "updated_at": "now()"
            }, on_conflict="slack_user_id").execute()
        except Exception as e:
            logger.error(f"Failed to save user session: {e}")


def clear_user_session(slack_user_id: str):
    """Clear session for a Slack user."""
    if slack_user_id in memory_sessions:
        del memory_sessions[slack_user_id]

    if supabase:
        try:
            supabase.table("slack_users").update({
                "session_id": None,
                "updated_at": "now()"
            }).eq("slack_user_id", slack_user_id).execute()
        except Exception as e:
            logger.error(f"Failed to clear user session: {e}")


def truncate_for_slack(text: str, max_length: int = 3900) -> str:
    """Truncate text to fit Slack's 4000 character limit."""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "\n\n_(Response truncated due to length)_"


def call_agent(user_id: str, message: str, username: str = None) -> str:
    """Call the marketing agent API (synchronous to avoid event loop conflicts)."""
    session_id = get_user_session(user_id)

    payload = {"message": message}
    if session_id:
        payload["session_id"] = session_id

    with httpx.Client(timeout=120.0) as client:
        response = client.post(
            f"{AGENT_API_URL}/agent/chat",
            json=payload
        )
        response.raise_for_status()
        data = response.json()

        # Save session for continuity
        if "session_id" in data:
            save_user_session(user_id, data["session_id"], username)

        content = data.get("content", "Sorry, I couldn't generate a response.")
        return truncate_for_slack(content)


def get_username(client, user_id: str) -> str:
    """Get username from Slack user ID."""
    try:
        result = client.users_info(user=user_id)
        if result["ok"]:
            return result["user"]["real_name"] or result["user"]["name"]
    except Exception:
        pass
    return None


@app.event("app_mention")
def handle_mention(event, say, client):
    """Handle @MarketingBot mentions in channels."""
    user_id = event["user"]
    text = event["text"]
    thread_ts = event.get("thread_ts") or event["ts"]
    username = get_username(client, user_id)

    # Remove the bot mention from the message
    message = text.split(">", 1)[-1].strip() if ">" in text else text

    if not message:
        say("Hi! How can I help with your marketing today?", thread_ts=thread_ts)
        return

    # Show typing indicator
    say("🤔 Thinking...", thread_ts=thread_ts)

    try:
        response = call_agent(user_id, message, username)
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
    username = get_username(client, user_id)

    if not message:
        return

    try:
        response = call_agent(user_id, message, username)
        say(response)
    except Exception as e:
        logger.error(f"Agent error: {e}")
        say("Sorry, something went wrong. Please try again.")


@app.command("/marketing")
def handle_slash_command(ack, respond, command, client):
    """Handle /marketing slash command."""
    ack()

    user_id = command["user_id"]
    message = command["text"]
    username = get_username(client, user_id)

    if not message:
        respond("Usage: `/marketing <your request>`\n\nExample: `/marketing Write a LinkedIn post about AI consulting`")
        return

    respond("🤔 Thinking...")

    try:
        response = call_agent(user_id, message, username)
        respond(response)
    except Exception as e:
        logger.error(f"Agent error: {e}")
        respond("Sorry, something went wrong. Please try again.")


@app.command("/clear")
def handle_clear(ack, respond, command):
    """Clear conversation history for the user."""
    ack()
    user_id = command["user_id"]

    clear_user_session(user_id)
    respond("✅ Conversation cleared! I've forgotten our previous chat.")


if __name__ == "__main__":
    # Socket Mode uses WebSocket - no public URL needed
    handler = SocketModeHandler(
        app,
        os.environ.get("SLACK_APP_TOKEN")
    )
    logger.info("Starting Slack bot in Socket Mode...")
    handler.start()
