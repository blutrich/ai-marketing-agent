# PRD: Autonomous AI Marketing Agent

## 1. Executive Summary

This PRD defines an autonomous AI marketing agent built with the Claude Agent SDK that can independently plan, create, and manage marketing content for Base44/Ofer Blutrich. Unlike the current webhook server (which is stateless and reactive), this agent has memory, tools, and the ability to pursue goals across multiple sessions.

The agent will leverage existing marketing skills (brand-voice, linkedin-viral, direct-response-copy, seo-content, geo-content) while adding autonomous capabilities: remembering past content, analyzing performance, and making decisions about what to create next.

**MVP Goal:** An agent that can autonomously manage a weekly content calendar - remembering what it created, analyzing what worked, and planning what comes next.

---

## 2. Mission

**Mission Statement:** Build an AI agent with persistent memory and autonomous decision-making that acts as a tireless marketing team member - not just generating content on demand, but proactively managing the entire content lifecycle.

**Core Principles:**
1. **Autonomy** - Agent decides what to do, not just how to do it
2. **Memory** - Remembers all past work and learns from results
3. **Goal-Oriented** - Works toward objectives, not just tasks
4. **Human-in-Loop** - Critical actions require approval
5. **Skill-Powered** - Leverages existing marketing skills for quality

---

## 3. Target Users

**Primary User: Ofer Blutrich (Founder/Consultant)**
- Technical comfort: High (developer background)
- Time available for marketing: Limited (focused on client work)
- Needs: Consistent content without daily involvement
- Pain points:
  - Forgetting to post regularly
  - Not tracking what content performed well
  - Starting from scratch each time

**Secondary User: Marketing Orchestrator (n8n/Zapier)**
- Technical integration via webhooks
- Needs: Reliable API for triggering agent actions
- Pain points: Stateless tools that don't remember context

---

## 4. MVP Scope

### In Scope (MVP)

**Core Agent Capabilities:**
- ✅ Persistent memory across sessions (conversation history, content log)
- ✅ Session resume - continue where left off
- ✅ Multi-turn reasoning and planning
- ✅ Goal pursuit with progress tracking

**Memory & Database:**
- ✅ Supabase integration for persistent storage
- ✅ Content log (what was created, when, performance)
- ✅ Conversation history (session continuity)
- ✅ User preferences and brand context

**Tools:**
- ✅ Read/Write/Edit files (content drafts)
- ✅ WebFetch (research, competitor analysis)
- ✅ Database queries (retrieve past content)
- ✅ Custom MCP tool: content_log (store/retrieve content)

**Endpoints:**
- ✅ POST /agent/chat - Stateful conversation with agent
- ✅ POST /agent/task - Assign goal, agent works autonomously
- ✅ GET /agent/status - Check what agent is working on
- ✅ GET /agent/history - Retrieve past sessions

### Out of Scope (Future)

**External Integrations:**
- ❌ Direct LinkedIn posting (use Gumloop/Zapier)
- ❌ Email sending (use external service)
- ❌ Analytics fetching (manual input for MVP)

**Advanced Features:**
- ❌ Multi-agent coordination
- ❌ Automatic scheduling/cron
- ❌ A/B testing automation
- ❌ Real-time performance monitoring

**Infrastructure:**
- ❌ Multi-tenant support
- ❌ User authentication (single-user MVP)
- ❌ Rate limiting (trust-based MVP)

---

## 5. User Stories

### Primary User Stories

1. **As Ofer, I want to tell the agent "plan this week's content" so that I have a full week of posts without thinking about each one.**
   - Example: "Plan LinkedIn content for this week focusing on AI consulting"
   - Agent remembers last week's posts, avoids repetition, creates variety

2. **As Ofer, I want the agent to remember what content performed well so that it creates more of what works.**
   - Example: Agent recalls "Posts about AI failures got 3x engagement"
   - Uses this to inform future content decisions

3. **As Ofer, I want to continue a conversation from yesterday so that I don't repeat context.**
   - Example: "Continue working on the campaign we discussed"
   - Agent loads previous session, picks up where left off

4. **As Ofer, I want to ask "what have you created this month?" so that I can see the agent's output.**
   - Example: Agent queries content_log, summarizes all posts created
   - Shows dates, topics, engagement (if logged)

5. **As Ofer, I want to give the agent a goal and let it work so that I can focus on client work.**
   - Example: "Create 5 LinkedIn posts about AI ROI"
   - Agent plans, drafts, stores - notifies when done

### Technical User Stories

6. **As an orchestrator (n8n), I want to trigger the agent via webhook so that I can automate workflows.**
   - POST to /agent/task with goal
   - Receive task_id, poll for completion

7. **As a developer, I want to see agent reasoning so that I can debug and improve.**
   - Agent exposes thinking/planning steps
   - Logs available for each session

---

## 6. Core Architecture & Patterns

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     FASTAPI SERVER                          │
│  /agent/chat    /agent/task    /agent/status               │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                  CLAUDE AGENT SDK                           │
│  ClaudeSDKClient (stateful)                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │   Skills    │  │    Tools    │  │   MCP Servers       │ │
│  │ (marketing) │  │ (built-in)  │  │ (database, custom)  │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                     SUPABASE                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │  sessions   │  │ content_log │  │   preferences       │ │
│  │  (history)  │  │  (output)   │  │   (brand context)   │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Directory Structure

```
server/
├── main.py                 # FastAPI app (existing, extend)
├── agent/
│   ├── __init__.py
│   ├── client.py           # ClaudeSDKClient wrapper
│   ├── memory.py           # Supabase memory operations
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── content_log.py  # MCP tool for content tracking
│   │   └── preferences.py  # MCP tool for brand context
│   └── sessions.py         # Session management
├── models/
│   ├── __init__.py
│   ├── requests.py         # Pydantic request models
│   └── responses.py        # Pydantic response models
├── db/
│   ├── __init__.py
│   ├── supabase.py         # Supabase client
│   └── migrations/         # SQL migrations
├── requirements.txt
├── Dockerfile
└── .env.example

.claude/skills/             # Existing skills (unchanged)
├── brand-voice/
├── linkedin-viral/
├── direct-response-copy/
├── seo-content/
└── geo-content/
```

### Key Design Patterns

1. **Stateful Client Pattern** - Use `ClaudeSDKClient` instead of `query()`
2. **Session Resume Pattern** - Store session IDs, resume with `resume="session-id"`
3. **MCP Tool Pattern** - Custom tools via MCP servers for database access
4. **Memory Abstraction** - All persistence through memory.py layer

---

## 7. Tools/Features

### Built-in Tools (Claude Agent SDK)

| Tool | Purpose | Usage |
|------|---------|-------|
| Read | Read files (drafts, references) | Research, review |
| Write | Create content files | Draft storage |
| Edit | Modify existing content | Revisions |
| Glob | Find files by pattern | Discovery |
| Grep | Search file contents | Research |
| WebFetch | Fetch web content | Competitor research |

### Custom MCP Tools

#### content_log Tool
```python
# Purpose: Track all content created by the agent

Operations:
- log_content(content, content_type, platform, metadata)
- get_recent_content(days=30)
- get_content_by_type(content_type)
- search_content(query)
- get_performance(content_id)  # If engagement data added
- update_performance(content_id, metrics)

Key Features:
- Auto-timestamps all entries
- Links to session that created it
- Supports performance tracking
```

#### preferences Tool
```python
# Purpose: Store and retrieve brand/user preferences

Operations:
- get_preference(key)
- set_preference(key, value)
- get_all_preferences()
- get_brand_context()  # Returns full brand info

Key Features:
- Hierarchical preferences (brand.voice, brand.topics, etc.)
- Version history for changes
- Defaults from skills if not set
```

#### session_memory Tool
```python
# Purpose: Manage conversation continuity

Operations:
- get_session_summary(session_id)
- list_recent_sessions(limit=10)
- get_session_context(session_id)  # What was discussed
- tag_session(session_id, tags)

Key Features:
- Auto-summarizes long sessions
- Searchable by tags/content
- Links to content created in session
```

---

## 8. Technology Stack

### Backend
- **Python 3.11+** - Runtime
- **FastAPI 0.109+** - Web framework
- **Claude Agent SDK 0.1.20+** - Agent infrastructure
- **Uvicorn** - ASGI server

### Database
- **Supabase** - PostgreSQL + Auth + Realtime
  - `supabase-py` - Python client

### Dependencies
```
# Core
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
pydantic>=2.0.0
claude-agent-sdk>=0.1.0

# Database
supabase>=2.0.0

# Utilities
httpx>=0.26.0
python-dotenv>=1.0.0
```

### Third-Party Integrations
- **Supabase** - Database and auth
- **Anthropic API** - Claude models (via SDK)

---

## 9. Security & Configuration

### Environment Variables

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-...
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJ...

# Optional
PORT=8000
MAX_TURNS=20
MAX_BUDGET_USD=5.0
SKILLS_DIR=/app
```

### Security Scope

**In Scope:**
- ✅ API key management via environment
- ✅ Supabase Row Level Security (RLS)
- ✅ Input validation (Pydantic)
- ✅ Tool permission controls

**Out of Scope (MVP):**
- ❌ Multi-user authentication
- ❌ Rate limiting
- ❌ Audit logging
- ❌ Encryption at rest

### Deployment
- **Platform:** Railway (or any container host)
- **Container:** Docker with Python 3.11
- **Scaling:** Single instance for MVP

---

## 10. API Specification

### POST /agent/chat

Stateful conversation with the agent.

**Request:**
```json
{
  "message": "Plan this week's LinkedIn content",
  "session_id": "optional-resume-session-id"
}
```

**Response:**
```json
{
  "response": "I'll plan your LinkedIn content for this week...",
  "session_id": "session-abc123",
  "metadata": {
    "cost_usd": 0.05,
    "duration_ms": 8500,
    "tools_used": ["content_log", "preferences"]
  }
}
```

### POST /agent/task

Assign autonomous task (fire-and-forget).

**Request:**
```json
{
  "goal": "Create 5 LinkedIn posts about AI ROI",
  "constraints": {
    "max_turns": 30,
    "max_budget_usd": 2.0
  },
  "webhook_url": "https://n8n.example.com/callback"
}
```

**Response:**
```json
{
  "task_id": "task-xyz789",
  "status": "started",
  "session_id": "session-abc123"
}
```

### GET /agent/status/{task_id}

Check task progress.

**Response:**
```json
{
  "task_id": "task-xyz789",
  "status": "in_progress",
  "progress": "Created 3/5 posts",
  "current_step": "Drafting post about cost savings",
  "started_at": "2025-01-20T10:00:00Z",
  "cost_so_far_usd": 0.15
}
```

### GET /agent/history

List past sessions and content.

**Response:**
```json
{
  "sessions": [
    {
      "session_id": "session-abc123",
      "started_at": "2025-01-20T10:00:00Z",
      "summary": "Planned weekly LinkedIn content",
      "content_created": 5
    }
  ],
  "total_content": 23,
  "total_sessions": 8
}
```

---

## 11. Success Criteria

### MVP Success Definition

The agent is successful when Ofer can:
1. Start a conversation, close it, return days later, and continue
2. Ask "what did we create last month?" and get accurate answer
3. Say "plan this week" and receive varied, non-repetitive content
4. See the agent's reasoning and planning process

### Functional Requirements

- ✅ Agent maintains conversation state across sessions
- ✅ Agent remembers all content it has created
- ✅ Agent can query its own history
- ✅ Agent uses skills appropriately for content type
- ✅ Agent plans multi-step tasks before executing
- ✅ Session can be resumed by ID
- ✅ Tasks can run autonomously with status polling
- ✅ Webhook callback on task completion

### Quality Indicators

- Response time < 30s for conversational turns
- Memory queries < 500ms
- No duplicate content within 30-day window
- Skills applied correctly 95%+ of time

---

## 12. Implementation Phases

### Phase 1: Stateful Foundation (Week 1)

**Goal:** Replace `query()` with `ClaudeSDKClient`, add session persistence.

**Deliverables:**
- ✅ ClaudeSDKClient wrapper in `agent/client.py`
- ✅ Session storage in Supabase
- ✅ `/agent/chat` endpoint with session resume
- ✅ Basic session history retrieval

**Validation:**
- Can start conversation, close terminal, resume next day
- Session ID persists and loads correctly

### Phase 2: Memory & Tools (Week 2)

**Goal:** Add content logging and custom MCP tools.

**Deliverables:**
- ✅ Supabase schema for content_log, preferences
- ✅ content_log MCP tool
- ✅ preferences MCP tool
- ✅ Agent can query its own history
- ✅ `/agent/history` endpoint

**Validation:**
- Agent remembers content it created
- "What did I create last week?" works correctly

### Phase 3: Autonomous Tasks (Week 3)

**Goal:** Fire-and-forget goals with progress tracking.

**Deliverables:**
- ✅ `/agent/task` endpoint
- ✅ `/agent/status` endpoint
- ✅ Background task execution
- ✅ Webhook callback on completion
- ✅ Progress tracking in database

**Validation:**
- Can assign goal, walk away, check status
- Webhook fires when complete

### Phase 4: Polish & Deploy (Week 4)

**Goal:** Production-ready deployment.

**Deliverables:**
- ✅ Error handling and retry logic
- ✅ Logging and observability
- ✅ Updated Dockerfile
- ✅ Railway deployment
- ✅ Documentation

**Validation:**
- Runs reliably on Railway
- Handles errors gracefully
- Logs useful for debugging

---

## 13. Future Considerations

### Post-MVP Enhancements

1. **Performance Analytics Integration**
   - Connect LinkedIn analytics
   - Auto-log engagement metrics
   - Agent learns from performance

2. **Proactive Scheduling**
   - Cron-triggered daily planning
   - "Good morning, here's today's post"
   - Autonomous posting approval flow

3. **Multi-Platform Support**
   - Twitter/X content adaptation
   - Email newsletter generation
   - Blog post drafting

4. **Advanced Memory**
   - Semantic search over past content
   - Topic clustering
   - Trend detection

### Integration Opportunities

- **Gumloop** - Trigger agent tasks from visual workflows
- **Notion** - Store content calendar
- **Google Analytics** - Website performance data
- **HubSpot** - Lead correlation with content

---

## 14. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| **SDK API changes** | High - breaks agent | Pin SDK version, test before upgrade |
| **Supabase downtime** | Medium - no memory | Local cache fallback, graceful degradation |
| **Cost overrun** | Medium - budget | max_budget_usd limits, cost alerts |
| **Context window limits** | Medium - long sessions | Summarize old turns, sliding window |
| **Repetitive content** | Low - quality | content_log deduplication checks |

---

## 15. Appendix

### Related Documents

- `.agents/AI-Marketing-System-PRD.md` - Overall system architecture
- `.agents/commands/create-prd.md` - PRD template
- `server/README.md` - Current webhook server docs

### Key Dependencies

- [Claude Agent SDK (Python)](https://github.com/anthropics/claude-agent-sdk-python)
- [Supabase Python Client](https://github.com/supabase-community/supabase-py)
- [FastAPI](https://fastapi.tiangolo.com/)

### Database Schema (Supabase)

```sql
-- Sessions table
CREATE TABLE sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id TEXT UNIQUE NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  summary TEXT,
  tags TEXT[],
  metadata JSONB
);

-- Content log table
CREATE TABLE content_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id TEXT REFERENCES sessions(session_id),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  content_type TEXT NOT NULL,
  platform TEXT,
  content TEXT NOT NULL,
  metadata JSONB,
  performance JSONB
);

-- Preferences table
CREATE TABLE preferences (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  key TEXT UNIQUE NOT NULL,
  value JSONB NOT NULL,
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tasks table
CREATE TABLE tasks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  task_id TEXT UNIQUE NOT NULL,
  session_id TEXT REFERENCES sessions(session_id),
  goal TEXT NOT NULL,
  status TEXT DEFAULT 'pending',
  progress TEXT,
  started_at TIMESTAMPTZ,
  completed_at TIMESTAMPTZ,
  webhook_url TEXT,
  result JSONB
);
```
