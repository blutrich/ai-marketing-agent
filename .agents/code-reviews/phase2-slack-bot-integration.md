# Code Review: Phase 2 - Slack Bot Integration

**Date:** 2026-01-20
**Reviewer:** Claude Code
**Scope:** Slack bot integration with persistent user sessions

---

## Summary

Phase 2 adds a Slack bot interface for the marketing agent, allowing non-technical team members to interact via DM, @mentions, and slash commands. User sessions are persisted in Supabase to maintain conversation context.

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 2 |
| Medium | 3 |
| Low | 3 |

**Overall Assessment:** The implementation is solid and functional. No critical issues. High-priority items relate to async/sync mixing and error message exposure.

---

## High Priority Issues

### 1. Blocking asyncio.run() in Sync Event Handlers

**File:** `server/slack_bot.py:146-147, 169-170, 193-194`

```python
@app.event("app_mention")
def handle_mention(event, say, client):
    # ...
    import asyncio
    response = asyncio.run(call_agent(user_id, message, username))
```

**Problem:** Using `asyncio.run()` inside synchronous Slack Bolt handlers creates a new event loop each time. This:
- Blocks the thread while waiting
- May cause issues under high load
- Prevents concurrent message processing

**Recommendation:** Use `@app.event` async handlers with the async Bolt adapter:
```python
from slack_bolt.async_app import AsyncApp

app = AsyncApp(token=os.environ.get("SLACK_BOT_TOKEN"))

@app.event("app_mention")
async def handle_mention(event, say, client):
    response = await call_agent(user_id, message, username)
    await say(response, thread_ts=thread_ts)
```

**Impact:** Medium for MVP, but should be fixed before scaling to multiple users.

---

### 2. "Thinking..." Message Never Updated

**File:** `server/slack_bot.py:143`

```python
# Show typing indicator
say("Thinking...", thread_ts=thread_ts)

try:
    response = asyncio.run(call_agent(user_id, message, username))
    say(response, thread_ts=thread_ts)  # Posts NEW message
```

**Problem:** The "Thinking..." message is never deleted or updated. Users see both the thinking message and the response, cluttering the conversation.

**Fix:** Use `chat.update` to replace the message:
```python
thinking_msg = say("Thinking...", thread_ts=thread_ts)
# ...
client.chat_update(
    channel=event["channel"],
    ts=thinking_msg["ts"],
    text=response
)
```

---

## Medium Priority Issues

### 3. Supabase Fallback Logic May Cause Confusion

**File:** `server/slack_bot.py:48-59`

```python
def get_user_session(slack_user_id: str) -> str | None:
    if supabase:
        try:
            result = supabase.table("slack_users").select("session_id").eq(...)
            if result.data and result.data[0].get("session_id"):
                return result.data[0]["session_id"]
        except Exception as e:
            logger.error(f"Failed to get user session: {e}")
    return memory_sessions.get(slack_user_id)  # Falls back silently
```

**Problem:** When Supabase fails, the code silently falls back to in-memory storage. This means:
- Users lose their session context on bot restart
- Behavior is inconsistent depending on DB state
- No indication to user that persistence is degraded

**Recommendation:** Log a warning when falling back, consider notifying on consistent failures.

---

### 4. Error Messages Expose Internal Details

**File:** `server/slack_bot.py:149-151, 172-174, 196-198`

```python
except Exception as e:
    logger.error(f"Agent error: {e}")
    say(f"Sorry, something went wrong. Please try again.", thread_ts=thread_ts)
```

**Status:** Good - error messages are user-friendly and don't expose internals.

However, the logger.error should include more context:

**Improvement:**
```python
logger.error(f"Agent error for user {user_id}: {e}", exc_info=True)
```

---

### 5. Bot Mention Parsing is Fragile

**File:** `server/slack_bot.py:136`

```python
message = text.split(">", 1)[-1].strip() if ">" in text else text
```

**Problem:** This assumes the bot mention format is always `<@BOTID>`. Edge cases:
- Multiple mentions: `<@BOTID> hi <@USERID>`
- URLs in message: `Check <https://example.com|this link>`
- No mention (edge case)

**Recommendation:** Use a regex or Slack's built-in mention parsing:
```python
import re
message = re.sub(r'<@[A-Z0-9]+>', '', text).strip()
```

---

## Low Priority Issues

### 6. Import Inside Function

**File:** `server/slack_bot.py:146, 169, 193`

```python
def handle_mention(event, say, client):
    # ...
    import asyncio  # Imported inside function
    response = asyncio.run(call_agent(...))
```

**Problem:** Importing inside function body is unconventional. While Python caches imports, it's cleaner at module level.

**Fix:** Move to top of file:
```python
import asyncio
```

---

### 7. Hardcoded Typing Indicator Emoji

**File:** `server/slack_bot.py:143, 190`

```python
say("Thinking...", thread_ts=thread_ts)
respond("Thinking...")
```

**Recommendation:** Use Slack's native typing indicator or a consistent emoji/message constant:
```python
THINKING_MESSAGE = ":hourglass_flowing_sand: Thinking..."
```

---

### 8. No Graceful Shutdown Handler

**File:** `server/slack_bot.py:211-218`

```python
if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
    logger.info("Starting Slack bot in Socket Mode...")
    handler.start()
```

**Problem:** No signal handlers for graceful shutdown (SIGTERM from Railway).

**Recommendation:**
```python
import signal

def shutdown_handler(signum, frame):
    logger.info("Shutting down gracefully...")
    handler.close()
    sys.exit(0)

signal.signal(signal.SIGTERM, shutdown_handler)
signal.signal(signal.SIGINT, shutdown_handler)
```

---

## Code Quality Observations

### Positive Patterns

1. **Proper Error Logging:** All database and agent errors are logged
2. **User-Friendly Errors:** Error messages don't expose technical details
3. **Session Persistence:** Smart fallback from Supabase to memory
4. **Clean Separation:** Slack bot is decoupled from agent - uses HTTP API
5. **Socket Mode:** No public URL required, simplifies deployment
6. **Username Capture:** Stores Slack username for agent context

### Phase 1 Issues Fixed

Several issues from Phase 1 review have been addressed:

| Issue | Status |
|-------|--------|
| Dockerfile copies all modules | Fixed |
| .env.example has Supabase vars | Fixed |
| Webhook URL validation | Fixed (HttpUrl) |
| DB error handling in memory.py | Fixed |
| datetime.utcnow() deprecated | Fixed |

---

## Files Reviewed

| File | Lines | Status |
|------|-------|--------|
| `server/slack_bot.py` | 219 | Has issues |
| `server/Dockerfile.slack` | 29 | OK |
| `slack-app-manifest.yaml` | 39 | OK |
| `server/.env.example` | 24 | OK |
| `server/requirements.txt` | 20 | OK |
| `server/agent/client.py` | 300 | OK (reviewed in Phase 1) |
| `server/agent/memory.py` | 359 | OK (improved since Phase 1) |

---

## Dockerfile.slack Review

**File:** `server/Dockerfile.slack`

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD pgrep -f "python slack_bot.py" || exit 1
```

**Observation:** Health check uses `pgrep` which is appropriate for a long-running Socket Mode process (no HTTP endpoint). This is correct.

**Minor:** Consider adding memory/connection health check if bot should report degraded state.

---

## Security Review

| Item | Status | Notes |
|------|--------|-------|
| Slack tokens in env vars | OK | Not hardcoded |
| Bot token validation | OK | Slack Bolt handles this |
| User input sanitization | OK | Slack escapes by default |
| Rate limiting | N/A | Slack handles rate limiting |
| SSRF via webhook | N/A | Not exposed in Slack bot |

---

## Deployment Checklist

Before deploying to Railway:

- [ ] Create new Railway service for Slack bot
- [ ] Set Dockerfile path to `server/Dockerfile.slack`
- [ ] Add environment variables:
  - `SLACK_BOT_TOKEN` (xoxb-...)
  - `SLACK_APP_TOKEN` (xapp-...)
  - `AGENT_API_URL` (Railway agent URL)
  - `SUPABASE_URL`
  - `SUPABASE_KEY`
- [ ] Create `slack_users` table in Supabase (if not exists)
- [ ] Verify Slack app has correct scopes and events enabled
- [ ] Test all interaction patterns (DM, mention, slash command)

---

## Recommendations Summary

### Should Fix Before Production

1. Replace "Thinking..." with updatable message
2. Add exc_info to error logging

### Should Fix for Scale

3. Convert to async Slack Bolt handlers
4. Improve mention parsing robustness
5. Add graceful shutdown handler

### Consider for Future

6. Add health metrics/monitoring
7. Implement user rate limiting (beyond Slack's)
8. Add /help command for discoverability

---

## Database Schema Addition

The `slack_users` table is required for this feature:

```sql
CREATE TABLE slack_users (
    id SERIAL PRIMARY KEY,
    slack_user_id TEXT UNIQUE NOT NULL,
    session_id TEXT,
    slack_username TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_slack_users_slack_user_id ON slack_users(slack_user_id);
```

---

## Conclusion

The Slack bot integration is well-designed and functional. The decoupled architecture (Slack bot -> HTTP API -> Agent) is clean and allows independent scaling. No critical issues block deployment.

Key strengths:
- Simple setup with Socket Mode (no public URL)
- Per-user session persistence
- Clean error handling
- Proper separation of concerns

Primary improvement area:
- Async handling for better concurrency
