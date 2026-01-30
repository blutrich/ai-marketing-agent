# AI Marketing Agent

> Skills-based marketing content generation system.

## Quick Start

```bash
# Start local server
cd server && source venv/bin/activate
SKILLS_DIR=$(pwd)/.. uvicorn server.main:app --reload --port 8000

# Test health
curl http://localhost:8000/health | jq

# Generate content
curl -X POST http://localhost:8000/generate-content \
  -H "Content-Type: application/json" \
  -d '{"content_type": "linkedin", "prompt": "Your topic here"}'
```

## Skills Architecture

Skills live in two locations:
- `.agents/skills/` - Development versions (full documentation, 9-section template)
- `.claude/skills/` - Production versions (compressed for deployment)

### Adding a New Skill (THREE steps required)

1. **Create skill files:**
   - `.agents/skills/[name]/skill.md` (development - use template from `.agents/skills/_template/`)
   - `.claude/skills/[name]/SKILL.md` (production - compressed format)

2. **Add server routing in `server/main.py:build_prompt()`:**
   ```python
   "[content-type]": "Use the [skill-name] skill..."
   ```

3. **Test production endpoint:**
   ```bash
   curl -X POST $URL/generate-content \
     -H "Content-Type: application/json" \
     -d '{"content_type": "[type]", "prompt": "test"}'
   ```

**CRITICAL:** A skill is NOT complete until ALL THREE steps are done. The `/health` endpoint checks skill file presence, but content generation requires server routing.

## Available Content Types

| Type | Skill | Purpose |
|------|-------|---------|
| `linkedin` | linkedin-viral | LinkedIn posts with hooks and engagement patterns |
| `email` | direct-response-copy | THE SLIDE framework emails |
| `seo` | seo-content | Search-optimized content |
| `geo` | geo-content | AI citation optimization (LLM discovery) |
| `direct-response` | direct-response-copy | Conversion copy |
| `landing-page` | landing-page-architecture | 8-Section Framework landing pages |
| `general` | brand-voice | Default consistent tone (fallback) |

## Skill Dependencies

```
FOUNDATION: brand-voice
    |
    v
EXECUTION: direct-response-copy, seo-content, landing-page-architecture
    |
    v
PLATFORM: linkedin-viral, geo-content
```

All skills should maintain brand voice consistency. Platform-specific skills build on execution skills.

## Server Architecture

**Key Files:**
- `server/main.py` - FastAPI application with content generation endpoints
- `server/main.py:125-149` - Content type routing (hints for skill activation)
- `server/main.py:build_prompt()` - Prompt construction with skill hints

**Endpoints:**
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | API info |
| `/health` | GET | Health check with skills_loaded list |
| `/generate-content` | POST | Stateless content generation |
| `/agent/chat` | POST | Stateful chat |
| `/agent/task` | POST | Background task |
| `/agent/status/{task_id}` | GET | Task status |
| `/agent/history` | GET | Conversation history |

## Available Commands

### Core Workflow
- `/plan-feature` - Create comprehensive implementation plan
- `/execute` - Execute a plan file
- `/prime` - Load project context

### Validation
- `/validate` - Run full validation suite
- `/code-review` - Technical code review
- `/system-review` - Process improvement analysis

### Skills
- `/add-skill <name> <type>` - Create new skill with full server integration

### Git
- `/commit` - Create git commit

## Directory Structure

```
.
├── CLAUDE.md              # This file - project documentation
├── server/
│   ├── main.py            # FastAPI application
│   └── venv/              # Python virtual environment
├── .claude/
│   └── skills/            # Production skill files
│       ├── brand-voice/
│       ├── direct-response-copy/
│       ├── linkedin-viral/
│       ├── seo-content/
│       ├── geo-content/
│       ├── marketing-ideas/
│       └── landing-page-architecture/
└── .agents/
    ├── skills/            # Development skill files
    │   └── _template/     # Skill template (9-section)
    ├── commands/          # Command definitions
    │   ├── core_piv_loop/ # Core workflow commands
    │   └── skills/        # Skill management commands
    └── plans/             # Generated implementation plans
```

## Development Workflow

1. **Plan first:** Use `/plan-feature` to create implementation plan
2. **Execute:** Use `/execute` to implement the plan
3. **Validate:** Run validation commands from the plan
4. **Review:** Use `/code-review` for quality check
5. **Commit:** Use `/commit` when ready

## Testing Skills Locally

```bash
# 1. Start server
cd server && source venv/bin/activate
SKILLS_DIR=$(pwd)/.. uvicorn server.main:app --port 8000

# 2. Check skills loaded
curl http://localhost:8000/health | jq '.skills_loaded'

# 3. Test specific content type
curl -X POST http://localhost:8000/generate-content \
  -H "Content-Type: application/json" \
  -d '{"content_type": "landing-page", "prompt": "SaaS product for time tracking"}'
```

---

*Last updated: 2026-01-21*
