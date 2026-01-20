# AI Marketing Content Generator

Webhook server for generating marketing content using Claude Agent SDK with skills.

## Architecture

```
Orchestrator (n8n/Zapier/Make/Base44)
         │
         ▼ POST /generate-content
┌─────────────────────────────────┐
│     FastAPI Webhook Server      │
│  ┌───────────────────────────┐  │
│  │   Claude Agent SDK        │  │
│  │   setting_sources=project │  │
│  └───────────────────────────┘  │
│  Skills from .claude/skills/    │
│  - brand-voice                  │
│  - linkedin-viral               │
│  - direct-response-copy         │
│  - seo-content                  │
│  - geo-content                  │
└─────────────────────────────────┘
         │
         ▼ JSON Response
   Generated Content
```

## Local Development

### Prerequisites

- Python 3.11+
- Claude Code CLI (`npm install -g @anthropic-ai/claude-code`)
- Anthropic API key

### Setup

1. Create virtual environment:
   ```bash
   cd server
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set environment variables:
   ```bash
   cp .env.example .env
   # Edit .env and add your ANTHROPIC_API_KEY
   ```

4. Run the server:
   ```bash
   # From project root (not server/)
   cd ..
   SKILLS_DIR=$(pwd) uvicorn server.main:app --reload --port 8000
   ```

### Testing Locally

Health check:
```bash
curl http://localhost:8000/health
```

Generate content:
```bash
curl -X POST http://localhost:8000/generate-content \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a LinkedIn post about AI consulting services",
    "content_type": "linkedin"
  }'
```

## Railway Deployment

### One-Click Deploy

1. Fork this repository to your GitHub account

2. Go to [Railway](https://railway.app) and create a new project

3. Select "Deploy from GitHub repo" and choose your fork

4. Add environment variable:
   - `ANTHROPIC_API_KEY`: Your Anthropic API key

5. Railway will automatically:
   - Detect the Dockerfile
   - Build the image
   - Deploy the service
   - Provide a public URL

### Manual Configuration

If needed, set these environment variables in Railway:

| Variable | Default | Description |
|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | (required) | Your Anthropic API key |
| `PORT` | 8000 | Server port (Railway sets this automatically) |
| `SKILLS_DIR` | /app | Directory containing .claude/skills/ |
| `MAX_TURNS` | 10 | Maximum agent turns per request |
| `MAX_BUDGET_USD` | 1.0 | Maximum cost per request |

## API Endpoints

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "skills_loaded": ["brand-voice", "linkedin-viral", "direct-response-copy", "seo-content", "geo-content"],
  "skills_directory": "/app/.claude/skills"
}
```

### POST /generate-content

Generate marketing content.

**Request:**
```json
{
  "prompt": "Write a LinkedIn post about AI consulting services",
  "content_type": "linkedin",
  "additional_context": "Target audience: CTOs at mid-size companies"
}
```

**Content Types:**
- `linkedin` - Uses linkedin-viral skill
- `email` - Uses direct-response-copy skill
- `seo` - Uses seo-content skill
- `geo` - Uses geo-content skill
- `direct-response` - Uses direct-response-copy skill
- `general` - Uses brand-voice skill

**Response:**
```json
{
  "content": "Generated marketing content...",
  "metadata": {
    "is_error": false,
    "cost_usd": 0.0234,
    "duration_ms": 5432,
    "content_type": "linkedin"
  }
}
```

### Stateful Agent Endpoints

#### POST /agent/chat

Stateful conversation with the agent. The agent remembers previous messages in the session.

**Request:**
```json
{
  "message": "Plan this week's LinkedIn content",
  "session_id": "session-abc123"
}
```

- `message` (required): The message to send to the agent
- `session_id` (optional): Session ID to resume a previous conversation

**Response:**
```json
{
  "content": "Here's your content plan...",
  "session_id": "session-abc123",
  "metadata": {
    "is_error": false,
    "cost_usd": 0.05,
    "duration_ms": 3200
  }
}
```

#### POST /agent/task

Assign an autonomous task to the agent. The agent will work toward the goal and track progress.

**Request:**
```json
{
  "goal": "Create 5 LinkedIn posts about AI ROI",
  "webhook_url": "https://your-app.com/webhook",
  "max_turns": 20,
  "max_budget_usd": 5.0
}
```

- `goal` (required): The goal for the agent to achieve
- `webhook_url` (optional): URL to call when task completes
- `max_turns` (optional): Override default max turns
- `max_budget_usd` (optional): Override default max budget

**Response:**
```json
{
  "task_id": "task-abc123",
  "session_id": "session-xyz789",
  "status": "in_progress",
  "message": "Task in_progress"
}
```

#### GET /agent/status/{task_id}

Check the status of an autonomous task.

**Response:**
```json
{
  "task_id": "task-abc123",
  "status": "completed",
  "progress": "Created 5 posts",
  "started_at": "2024-01-15T10:00:00Z",
  "completed_at": "2024-01-15T10:05:00Z",
  "cost_usd": 0.15,
  "result": { "posts_created": 5 }
}
```

#### GET /agent/history

Get agent history: recent sessions and content created.

**Query Parameters:**
- `limit` (optional): Maximum number of items to return (default: 20)

**Response:**
```json
{
  "sessions": [
    {
      "session_id": "session-abc123",
      "created_at": "2024-01-15T10:00:00Z",
      "summary": "LinkedIn content planning",
      "tags": ["linkedin", "content"]
    }
  ],
  "content": [
    {
      "id": "uuid",
      "created_at": "2024-01-15T10:05:00Z",
      "content_type": "linkedin",
      "platform": "linkedin",
      "title": "AI ROI Post",
      "preview": "First 100 characters..."
    }
  ],
  "stats": {
    "total_sessions": 42,
    "total_content": 156,
    "total_tasks": 23
  }
}
```

## Skills

Skills are loaded from `.claude/skills/` directory:

| Skill | Purpose |
|-------|---------|
| `brand-voice` | Consistent tone and messaging |
| `linkedin-viral` | LinkedIn hooks and engagement patterns |
| `direct-response-copy` | THE SLIDE framework for conversions |
| `seo-content` | Search engine optimization |
| `geo-content` | AI citation and LLM discovery |

## Integration Examples

### n8n Webhook

1. Create HTTP Request node
2. Method: POST
3. URL: `https://your-railway-url.up.railway.app/generate-content`
4. Body:
   ```json
   {
     "prompt": "{{ $json.topic }}",
     "content_type": "linkedin"
   }
   ```

### Zapier

1. Add Webhooks by Zapier action
2. Method: POST
3. URL: Your Railway URL + `/generate-content`
4. Data: Map your trigger data to prompt

### Make (Integromat)

1. Add HTTP module
2. Method: POST
3. URL: Your Railway URL + `/generate-content`
4. Body type: JSON
5. Map fields to request body

## Cost Estimation

| Component | Cost |
|-----------|------|
| Railway | ~$5/month (Hobby) |
| Claude API | ~$0.01-0.05 per generation |
| **Total** | ~$10-25/month for moderate usage |

## Troubleshooting

### Skills not loading

Check that:
1. Skills exist at `SKILLS_DIR/.claude/skills/`
2. Each skill has a `SKILL.md` file
3. `setting_sources=["project"]` is set in options

### CLI not found

The Dockerfile installs Claude Code CLI. If running locally:
```bash
npm install -g @anthropic-ai/claude-code
```

### API key errors

Ensure `ANTHROPIC_API_KEY` is set in environment variables.
