# Code Review: Phase 1 - Stateful Agent Implementation

**Date:** 2026-01-20
**Reviewer:** Claude Code
**Scope:** server/ directory (new agent implementation with Supabase memory)

---

## Summary

Phase 1 implementation adds stateful agent capabilities with Supabase-backed memory. The code is functional but has several issues that should be addressed before production deployment.

| Severity | Count |
|----------|-------|
| Critical | 3 |
| High | 4 |
| Medium | 4 |
| Low | 4 |

---

## Critical Issues

### 1. Dockerfile Incomplete - Missing Module Copies

**File:** `server/Dockerfile:30`

```dockerfile
# Only copies main.py but app requires agent/, db/, models/
COPY server/main.py /app/main.py
```

**Problem:** The Dockerfile only copies `main.py`, but the application now imports from `agent/`, `db/`, and `models/` modules. Deployment will fail.

**Fix:**
```dockerfile
# Copy entire server directory
COPY server/ /app/
```

---

### 2. Missing Supabase Environment Variables in .env.example

**File:** `server/.env.example`

```
# Current - missing critical variables
ANTHROPIC_API_KEY=your_api_key_here
PORT=8000
SKILLS_DIR=/app
```

**Problem:** The `.env.example` file doesn't include `SUPABASE_URL` and `SUPABASE_KEY` which are required for the agent to function.

**Fix:**
```
# Required: Anthropic API key for Claude
ANTHROPIC_API_KEY=your_api_key_here

# Required: Supabase connection
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_service_role_key

# Server Configuration
PORT=8000
...
```

---

### 3. README.md Missing New Agent Endpoints

**File:** `server/README.md`

**Problem:** Documentation only covers `/health` and `/generate-content`. Missing documentation for:
- `POST /agent/chat`
- `POST /agent/task`
- `GET /agent/status/{task_id}`
- `GET /agent/history`

**Fix:** Update README.md with new endpoint documentation.

---

## High Priority Issues

### 4. No Error Handling for Database Operations

**File:** `server/agent/memory.py`

```python
def create_session(self, metadata: Optional[dict] = None) -> str:
    session_id = f"session-{uuid.uuid4().hex[:12]}"
    # No try/except - if Supabase fails, exception propagates
    self.client.table("sessions").insert({...}).execute()
    return session_id
```

**Problem:** All database operations assume success. Network issues, timeouts, or Supabase outages will cause unhandled exceptions.

**Recommendation:** Add try/except blocks with proper error handling and logging.

---

### 5. Synchronous Database Operations in Async Context

**File:** `server/agent/memory.py`

**Problem:** Using synchronous Supabase client methods inside an async FastAPI application can block the event loop, degrading performance under load.

**Recommendation:** Either:
1. Use `supabase-py` async client (if available)
2. Run database operations in a thread pool executor
3. Document this limitation for MVP

---

### 6. Race Condition in Task Creation

**File:** `server/main.py:311-324`

```python
session_id = agent_memory.create_session(metadata={...})
task_id = agent_memory.create_task(goal=request.goal, session_id=session_id, ...)
agent_memory.update_task(task_id, status="in_progress")
```

**Problem:** Three separate database operations with no transaction. If the process fails after creating session but before task, orphaned records remain.

**Recommendation:** Use a transaction or implement cleanup logic for partial failures.

---

### 7. Missing URL Validation for Webhook

**File:** `server/models/requests.py:29-32`

```python
webhook_url: Optional[str] = Field(
    default=None,
    description="Optional URL to call when task completes"
)
```

**Problem:** No validation that `webhook_url` is a valid URL format.

**Fix:**
```python
from pydantic import HttpUrl

webhook_url: Optional[HttpUrl] = Field(...)
```

---

## Medium Priority Issues

### 8. LIKE Pattern Injection Risk

**File:** `server/agent/memory.py:110-116`

```python
def search_content(self, query: str, limit: int = 20) -> list:
    result = self.client.table("content_log").select("*").ilike(
        "content", f"%{query}%"
    ).order("created_at", desc=True).limit(limit).execute()
```

**Problem:** Special LIKE characters (`%`, `_`) in user input are not escaped, allowing pattern manipulation.

**Recommendation:** Escape LIKE special characters:
```python
escaped_query = query.replace("%", "\\%").replace("_", "\\_")
```

---

### 9. Unused Import

**File:** `server/main.py:25`

```python
from pydantic import BaseModel, Field  # Field not used in this file
```

**Fix:** Remove unused `Field` import.

---

### 10. No Rate Limiting

**Problem:** API endpoints have no rate limiting, making them vulnerable to abuse.

**Recommendation:** Add rate limiting middleware (e.g., `slowapi`) before production.

---

### 11. No Authentication

**Problem:** All endpoints are publicly accessible. Anyone with the URL can use the agent and incur API costs.

**Recommendation:** Add API key authentication or OAuth for production:
```python
from fastapi.security import APIKeyHeader
api_key_header = APIKeyHeader(name="X-API-Key")
```

---

## Low Priority Issues

### 12. Deprecated datetime.utcnow()

**File:** `server/agent/memory.py:94, 187, 189`

```python
since = (datetime.utcnow() - timedelta(days=days)).isoformat()
```

**Problem:** `datetime.utcnow()` is deprecated in Python 3.12+.

**Fix:**
```python
from datetime import timezone
since = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
```

---

### 13. Magic Numbers for Truncation

**Files:**
- `server/agent/client.py:131` - `[:200]`
- `server/main.py:400` - `[:100]`
- `server/agent/client.py:249` - `[:1000]`

**Recommendation:** Extract to named constants:
```python
SUMMARY_MAX_LENGTH = 200
PREVIEW_MAX_LENGTH = 100
RESULT_MAX_LENGTH = 1000
```

---

### 14. TaskRequest max_turns/max_budget_usd Not Used

**File:** `server/models/requests.py:33-40`

```python
max_turns: Optional[int] = Field(...)
max_budget_usd: Optional[float] = Field(...)
```

These fields are defined but never used in the `/agent/task` endpoint.

---

### 15. Hardcoded allowed_tools

**File:** `server/agent/client.py:58`

```python
allowed_tools=["Read", "Glob", "Grep", "Write", "Edit", "WebFetch"],
```

**Recommendation:** Make this configurable via environment variable or constructor parameter.

---

## Files Reviewed

| File | Lines | Status |
|------|-------|--------|
| `server/main.py` | 418 | Has issues |
| `server/agent/client.py` | 265 | Has issues |
| `server/agent/memory.py` | 245 | Has issues |
| `server/agent/__init__.py` | 7 | OK |
| `server/db/supabase.py` | 27 | OK |
| `server/db/__init__.py` | 6 | OK |
| `server/models/requests.py` | 60 | Has issues |
| `server/models/responses.py` | 96 | OK |
| `server/models/__init__.py` | 32 | OK |
| `server/requirements.txt` | 17 | OK |
| `server/.env.example` | 14 | Has issues |
| `server/Dockerfile` | 45 | Has issues |
| `server/README.md` | 230 | Has issues |

---

## Recommendations Summary

### Must Fix Before Deployment
1. Update Dockerfile to copy all server modules
2. Add Supabase variables to .env.example
3. Add basic error handling for database operations

### Should Fix Soon
4. Update README.md with new endpoints
5. Add webhook URL validation
6. Implement basic rate limiting
7. Add API key authentication

### Consider for Future
8. Async database operations
9. Transaction support for multi-step operations
10. Configurable tool permissions

---

## Test Coverage

No automated tests exist. Recommend adding:
- Unit tests for memory operations
- Integration tests for API endpoints
- End-to-end tests for chat flow

---

## Conclusion

The Phase 1 implementation provides a solid foundation for a stateful marketing agent. The critical Dockerfile issue must be fixed before Railway deployment. Security improvements (auth, rate limiting) should be prioritized before making the service publicly accessible.
