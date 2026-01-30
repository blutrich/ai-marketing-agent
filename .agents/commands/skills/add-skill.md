---
description: Create a new skill with all required components and server integration
argument-hint: <skill-name> <content-type>
---

# Add Skill Command

Create a new skill with proper server integration. Ensures ALL THREE required steps are completed.

## Arguments

- `$1` - Skill name (kebab-case, e.g., "landing-page-architecture")
- `$2` - Content type for server routing (e.g., "landing-page")

## Process

### Step 1: Create Directories

```bash
mkdir -p .agents/skills/$1
mkdir -p .claude/skills/$1
```

### Step 2: Scaffold Development Version

Create `.agents/skills/$1/skill.md` using the 9-section template from `.agents/skills/_template/skill-template.md`:

1. UNDERSTAND - Problem Definition
2. EXPLORE - Failure Modes
3. RESEARCH - Domain Expertise
4. SYNTHESIZE - Core Framework
5. DRAFT - Skill Instructions
6. SELF-CRITIQUE - Quality Checklist
7. ITERATE - Improvement Log
8. TEST - Validation Scenarios
9. FINALIZE - Production Structure

**Ask the user for:**
- Skill purpose and domain
- Key principles/framework
- Example inputs and outputs

### Step 3: Create Production Version

Create `.claude/skills/$1/SKILL.md` with compressed format:

```markdown
# [Skill Name]

> [One-line description]

## When to Use
[Trigger conditions]

## Core Framework
[Essential process/steps]

## Quality Checklist
- [ ] [Criterion 1]
- [ ] [Criterion 2]

## Example
[Full example of excellent output]

## Integration
- **Depends on:** [dependencies]
- **Content type:** $2
```

### Step 4: Add Server Routing

Update `server/main.py:build_prompt()` content_type_hints dict:

```python
"$2": "Use the $1 skill...",
```

**Location:** `server/main.py` around line 127-135 (inside `content_type_hints` dict)

### Step 5: Validate End-to-End

```bash
# Check files exist
ls -la .agents/skills/$1/
ls -la .claude/skills/$1/

# Check server routing added
grep "$2" server/main.py

# Test locally
cd server && source venv/bin/activate
SKILLS_DIR=$(pwd)/.. uvicorn server.main:app --port 8000 &
sleep 3

# Verify skill loaded
curl http://localhost:8000/health | jq '.skills_loaded'

# Test content generation
curl -X POST http://localhost:8000/generate-content \
  -H "Content-Type: application/json" \
  -d "{\"content_type\": \"$2\", \"prompt\": \"Test the $1 skill\"}"

# Kill test server
pkill -f "uvicorn server.main:app"
```

## Output Checklist

Report completion status:

- [ ] Development version created (`.agents/skills/$1/skill.md`)
- [ ] Production version created (`.claude/skills/$1/SKILL.md`)
- [ ] Server routing added (`server/main.py`)
- [ ] Local health check shows skill loaded
- [ ] Local generate-content works with content type
- [ ] Ready for commit and deploy

## Common Issues

**Skill not in health check:**
- Verify `.claude/skills/$1/SKILL.md` exists (exact filename)
- Check SKILLS_DIR environment variable is set

**Content type not routing:**
- Verify entry added to `content_type_hints` dict in `server/main.py`
- Check for typos in content type string

**Server won't start:**
- Activate venv: `source server/venv/bin/activate`
- Check for syntax errors in main.py

## Example Usage

```bash
# Create a new "case-study" skill with content type "case-study"
/add-skill case-study case-study

# This will:
# 1. Create .agents/skills/case-study/skill.md
# 2. Create .claude/skills/case-study/SKILL.md
# 3. Add "case-study": "Use the case-study skill..." to server/main.py
# 4. Validate everything works
```

---

*Reference: See CLAUDE.md for full skills architecture documentation*
