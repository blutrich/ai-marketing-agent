# Feature: Integrate Marketing Skills Suite from External Repository

The following plan should be complete, but it's important that you validate documentation and codebase patterns and task sanity before you start implementing.

Pay special attention to naming of existing utils types and models. Import from the right files etc.

## Feature Description

Integrate 10 specialized marketing skills and brand data from `blutrich/base44-marketing-skills--Jun2026-with-remotion` into the Railway-deployed AI Marketing Agent. This creates a professional 17-skill marketing suite accessible via Slack integration.

## User Story

As a marketing team using the Slack integration
I want access to a complete suite of 17 specialized content skills
So that I can generate any type of marketing content (posts, slides, videos, diagrams, images) through a single agent

## Problem Statement

Current Railway agent has 7 skills focused on text content. Missing capabilities for:
- Twitter/X content generation
- PowerPoint presentations
- Excalidraw diagrams
- Video scripts (Remotion)
- AI image generation
- Brand system creation
- SOP documentation
- Meta-skills (skill creation)

## Solution Statement

Copy 10 skills and brand data from external repository, fix Docker path references, update server routing, and deploy to Railway. Result: 17-skill professional marketing suite.

## Feature Metadata

**Feature Type**: Enhancement
**Estimated Complexity**: Medium
**Primary Systems Affected**: Skills directory, Docker deployment, Server routing
**Dependencies**: External GitHub repository access

---

## CONTEXT REFERENCES

### Relevant Codebase Files IMPORTANT: YOU MUST READ THESE FILES BEFORE IMPLEMENTING!

- `server/Dockerfile` (line 23) - Pattern: `COPY .claude/skills/ /app/.claude/skills/`
- `server/Dockerfile` (line 40) - ENV: `SKILLS_DIR=/app`
- `server/main.py` (lines 125-149) - `build_prompt()` function with `content_type_hints` dictionary
- `server/main.py` (lines 127-135) - Current content type mappings to update
- `server/main.py` (lines 78-84) - Skills discovery in `lifespan()` function
- `.claude/skills/brand-voice/SKILL.md` - Foundation skill pattern
- `.claude/skills/linkedin-viral/SKILL.md` - Platform skill pattern

### External Repository Files to Copy

**From:** `https://github.com/blutrich/base44-marketing-skills--Jun2026-with-remotion`

**Skills (10):**
```
.claude/skills/linkedin-post/SKILL.md
.claude/skills/x-post/SKILL.md
.claude/skills/pptx-generator/SKILL.md
.claude/skills/base44-video/SKILL.md
.claude/skills/remotion/SKILL.md
.claude/skills/excalidraw-diagram/SKILL.md
.claude/skills/brand-voice-generator/SKILL.md
.claude/skills/skill-creator/SKILL.md
.claude/skills/sop-creator/SKILL.md
.claude/skills/nano-banana/SKILL.md
```

**Brand Data:**
```
brands/base44/
├── brand-system.md
├── brand.json
├── tone-of-voice.md
├── assets/
├── case-studies/
├── content-library/
├── facts/
└── feedback/
```

### New Files to Create/Copy

| Source | Destination |
|--------|-------------|
| External `.claude/skills/*` (10 dirs) | `.claude/skills/` |
| External `brands/` | `brands/` |

### Patterns to Follow

**Dockerfile COPY Pattern (line 23):**
```dockerfile
COPY .claude/skills/ /app/.claude/skills/
# Add after:
COPY brands/ /app/brands/
```

**Content Type Routing Pattern (main.py:127-135):**
```python
content_type_hints = {
    "linkedin": "Use the linkedin-viral skill...",
    # Pattern: "content-type": "Use the {skill-name} skill to {description}.",
}
```

**Path Reference Pattern in Skills:**
- External: `../../brands/base44/tone-of-voice.md`
- Docker: `/app/brands/base44/tone-of-voice.md`

---

## IMPLEMENTATION PLAN

### Phase 1: Clone and Copy Repository Content

Clone external repo and copy skills + brands to project.

**Tasks:**
- Clone external repository to temp location
- Copy all 10 skill directories to `.claude/skills/`
- Copy `brands/` directory to project root
- Verify file structure matches expected

### Phase 2: Fix Relative Paths in Skills

Update skills that reference brand data to use absolute Docker paths.

**Tasks:**
- Identify skills with `../../brands/` references
- Replace `../../brands/` with `/app/brands/`
- Verify all path references updated

### Phase 3: Update Docker Configuration

Add brands directory to Docker build.

**Tasks:**
- Add `COPY brands/` line to Dockerfile after skills copy
- Verify SKILLS_DIR environment variable covers both

### Phase 4: Update Server Routing

Add content type hints for new skills.

**Tasks:**
- Add 9 new content type mappings to `content_type_hints` dictionary
- Keep existing 7 mappings intact

### Phase 5: Testing & Deployment

Test locally then deploy to Railway.

**Tasks:**
- Start local server with SKILLS_DIR
- Verify 17 skills in /health response
- Test new content types via /generate-content
- Commit and push to trigger Railway deploy
- Verify production deployment

---

## STEP-BY-STEP TASKS

IMPORTANT: Execute every task in order, top to bottom. Each task is atomic and independently testable.

### 1. CREATE Clone external repository

```bash
git clone https://github.com/blutrich/base44-marketing-skills--Jun2026-with-remotion.git /tmp/marketing-skills
```

- **VALIDATE**: `ls /tmp/marketing-skills/.claude/skills/ | wc -l` (should be 10)

### 2. CREATE Copy brands directory to project

```bash
cp -r /tmp/marketing-skills/brands /Users/blutrich/Documents/DEV/Vibe\ Marketing\ Base44/brands
```

- **VALIDATE**: `ls brands/base44/` (should show brand.json, tone-of-voice.md, etc.)

### 3. CREATE Copy all 10 skills to .claude/skills/

```bash
cp -r /tmp/marketing-skills/.claude/skills/linkedin-post .claude/skills/
cp -r /tmp/marketing-skills/.claude/skills/x-post .claude/skills/
cp -r /tmp/marketing-skills/.claude/skills/pptx-generator .claude/skills/
cp -r /tmp/marketing-skills/.claude/skills/base44-video .claude/skills/
cp -r /tmp/marketing-skills/.claude/skills/remotion .claude/skills/
cp -r /tmp/marketing-skills/.claude/skills/excalidraw-diagram .claude/skills/
cp -r /tmp/marketing-skills/.claude/skills/brand-voice-generator .claude/skills/
cp -r /tmp/marketing-skills/.claude/skills/skill-creator .claude/skills/
cp -r /tmp/marketing-skills/.claude/skills/sop-creator .claude/skills/
cp -r /tmp/marketing-skills/.claude/skills/nano-banana .claude/skills/
```

- **VALIDATE**: `ls .claude/skills/ | wc -l` (should be 17)

### 4. UPDATE Fix relative paths in linkedin-post/SKILL.md

- **FILE**: `.claude/skills/linkedin-post/SKILL.md`
- **PATTERN**: Replace all `../../brands/` with `/app/brands/`
- **LINES TO FIX**:
  - `Read: ../../brands/base44/tone-of-voice.md` → `Read: /app/brands/base44/tone-of-voice.md`
  - `Read: ../../brands/base44/facts/metrics.md` → `Read: /app/brands/base44/facts/metrics.md`
  - `Read: ../../brands/base44/case-studies/index.md` → `Read: /app/brands/base44/case-studies/index.md`
  - `Read: ../../brands/base44/case-studies/giftmybook.md` → `Read: /app/brands/base44/case-studies/giftmybook.md`
  - `Read: ../../brands/base44/feedback/testimonials.md` → `Read: /app/brands/base44/feedback/testimonials.md`
  - `Read: ../../brands/base44/content-library/hooks.md` → `Read: /app/brands/base44/content-library/hooks.md`
  - `Read: ../../brands/base44/content-library/ctas.md` → `Read: /app/brands/base44/content-library/ctas.md`
- **VALIDATE**: `grep -c "../../brands" .claude/skills/linkedin-post/SKILL.md` (should be 0)

### 5. UPDATE Fix relative paths in x-post/SKILL.md (if present)

- **FILE**: `.claude/skills/x-post/SKILL.md`
- **PATTERN**: Replace all `../../brands/` with `/app/brands/`
- **VALIDATE**: `grep -c "../../brands" .claude/skills/x-post/SKILL.md` (should be 0)

### 6. UPDATE Fix relative paths in all other skills with brand references

- **SEARCH**: `grep -r "../../brands" .claude/skills/`
- **PATTERN**: Replace all `../../brands/` with `/app/brands/`
- **VALIDATE**: `grep -r "../../brands" .claude/skills/` (should return empty)

### 7. UPDATE server/Dockerfile - Add brands COPY

- **FILE**: `server/Dockerfile`
- **LOCATION**: After line 23 (`COPY .claude/skills/ /app/.claude/skills/`)
- **ADD**:
```dockerfile
COPY brands/ /app/brands/
```
- **VALIDATE**: `grep "COPY brands" server/Dockerfile` (should match)

### 8. UPDATE server/main.py - Add content type routing

- **FILE**: `server/main.py`
- **LOCATION**: Lines 127-135, inside `content_type_hints` dictionary
- **ADD** new entries:
```python
"linkedin-post": "Use the linkedin-post skill for authentic, anti-template LinkedIn content with specificity and genuine voice.",
"x-post": "Use the x-post skill for Twitter/X content with hooks and thread structures.",
"twitter": "Use the x-post skill for Twitter/X content with hooks and thread structures.",
"slides": "Use the pptx-generator skill for branded PowerPoint presentations.",
"presentation": "Use the pptx-generator skill for branded PowerPoint presentations.",
"video": "Use the base44-video skill for Remotion video script generation.",
"diagram": "Use the excalidraw-diagram skill for visual diagrams and flowcharts.",
"image": "Use the nano-banana skill for AI image generation with Gemini.",
"brand-setup": "Use the brand-voice-generator skill to create brand system files (colors, fonts, voice).",
"sop": "Use the sop-creator skill for runbooks and standard operating procedures.",
"skill": "Use the skill-creator skill to create new Claude Code skills.",
```
- **VALIDATE**: `grep -c "linkedin-post\|x-post\|pptx-generator" server/main.py` (should be 3+)

### 9. VALIDATE Local test - Start server

```bash
cd server && source venv/bin/activate
SKILLS_DIR=$(pwd)/.. uvicorn main:app --port 8000 &
sleep 3
```

- **VALIDATE**: Server starts without errors

### 10. VALIDATE Local test - Check skills loaded

```bash
curl http://localhost:8000/health | jq '.skills_loaded'
```

- **EXPECTED**: Array with 17 skills including: brand-voice, linkedin-viral, linkedin-post, x-post, pptx-generator, base44-video, remotion, excalidraw-diagram, brand-voice-generator, skill-creator, sop-creator, nano-banana, etc.

### 11. VALIDATE Local test - Test new content type

```bash
curl -X POST http://localhost:8000/generate-content \
  -H "Content-Type: application/json" \
  -d '{"content_type": "linkedin-post", "prompt": "create a post about Base44 success"}'
```

- **EXPECTED**: Response includes content with linkedin-post skill activation

### 12. CREATE Git commit and push

```bash
git add brands/ .claude/skills/ server/Dockerfile server/main.py
git commit -m "feat: Add 10 marketing skills and brand data from base44-marketing-skills repo

Integrated skills:
- linkedin-post (authentic LinkedIn content)
- x-post (Twitter/X content)
- pptx-generator (branded presentations)
- base44-video (Remotion video scripts)
- remotion (video generation)
- excalidraw-diagram (visual diagrams)
- brand-voice-generator (brand system creation)
- skill-creator (meta-skill for creating skills)
- sop-creator (runbooks/documentation)
- nano-banana (AI image generation)

Also added brands/base44/ with brand data, case studies, and content library.

Total skills: 17 (7 existing + 10 new)"
git push
```

- **VALIDATE**: Push succeeds, Railway auto-deploy triggers

### 13. VALIDATE Production - Check Railway deployment

```bash
# Wait 2-3 minutes for Railway deploy
curl https://ai-marketing-agent-production-60c7.up.railway.app/health | jq
```

- **EXPECTED**: `skills_loaded` array contains 17 skills

### 14. VALIDATE Production - Test new skill

```bash
curl -X POST https://ai-marketing-agent-production-60c7.up.railway.app/generate-content \
  -H "Content-Type: application/json" \
  -d '{"content_type": "linkedin-post", "prompt": "Write about Base44 GiftMyBook success"}'
```

- **EXPECTED**: Response with linkedin-post skill activated, authentic content

---

## TESTING STRATEGY

### Unit Tests

No unit tests required - this is a configuration/deployment change.

### Integration Tests

**Health Check:**
```bash
curl http://localhost:8000/health | jq '.skills_loaded | length'
# Expected: 17
```

**Content Generation per Content Type:**
```bash
for type in linkedin-post x-post slides diagram video brand-setup sop; do
  echo "Testing $type..."
  curl -s -X POST http://localhost:8000/generate-content \
    -H "Content-Type: application/json" \
    -d "{\"content_type\": \"$type\", \"prompt\": \"test\"}" | jq '.content | length > 0'
done
```

### Edge Cases

- [ ] Unknown content type falls back to "general" (brand-voice)
- [ ] Missing brand file doesn't crash skill (graceful degradation)
- [ ] Skills without brand references work unchanged

---

## VALIDATION COMMANDS

Execute every command to ensure zero regressions and 100% feature correctness.

### Level 1: File Structure

```bash
# Verify all 17 skills present
ls .claude/skills/ | wc -l
# Expected: 17

# Verify brands directory
ls brands/base44/
# Expected: brand.json, tone-of-voice.md, brand-system.md, assets/, case-studies/, etc.

# Verify no remaining relative paths
grep -r "../../brands" .claude/skills/
# Expected: (empty output)
```

### Level 2: Docker Build

```bash
cd server
docker build -t test-agent .
# Expected: Build succeeds

docker run --rm test-agent ls /app/brands/base44/
# Expected: brand.json, tone-of-voice.md, etc.

docker run --rm test-agent ls /app/.claude/skills/ | wc -l
# Expected: 17
```

### Level 3: Local Server

```bash
cd server && source venv/bin/activate
SKILLS_DIR=$(pwd)/.. uvicorn main:app --port 8000 &
sleep 3

curl http://localhost:8000/health | jq '.skills_loaded'
# Expected: 17-element array

pkill -f "uvicorn main:app"
```

### Level 4: Production

```bash
curl https://ai-marketing-agent-production-60c7.up.railway.app/health | jq
# Expected: skills_loaded with 17 skills

curl -X POST https://ai-marketing-agent-production-60c7.up.railway.app/generate-content \
  -H "Content-Type: application/json" \
  -d '{"content_type": "linkedin-post", "prompt": "test"}'
# Expected: Valid response
```

---

## ACCEPTANCE CRITERIA

- [x] All 10 new skills copied to `.claude/skills/`
- [ ] `brands/` directory copied to project root
- [ ] All relative paths (`../../brands/`) fixed to `/app/brands/`
- [ ] Dockerfile updated with `COPY brands/` line
- [ ] `main.py` updated with 9 new content type mappings
- [ ] Local server shows 17 skills in `/health`
- [ ] Local `/generate-content` works for new content types
- [ ] Railway deployment succeeds
- [ ] Production shows 17 skills in `/health`
- [ ] Production `/generate-content` works for new content types
- [ ] No regressions in existing 7 skills

---

## COMPLETION CHECKLIST

- [ ] External repo cloned
- [ ] All 10 skills copied
- [ ] brands/ directory copied
- [ ] Relative paths fixed in all skills
- [ ] Dockerfile updated
- [ ] main.py routing updated
- [ ] Local testing passed
- [ ] Git commit created
- [ ] Railway deployment triggered
- [ ] Production verification passed

---

## NOTES

### Skill Conflict Resolution

**brand-voice vs brand-voice-generator:**
- `brand-voice` (existing): APPLIES Base44 voice framework to content
- `brand-voice-generator` (new): CREATES brand system files (colors, fonts, voice docs)
- **Decision:** KEEP BOTH - They form a workflow (create brand → apply voice)

**linkedin-viral vs linkedin-post:**
- `linkedin-viral` (existing): Algorithm optimization, hooks, formatting rules
- `linkedin-post` (new): Anti-template philosophy, authentic voice, specificity
- **Decision:** KEEP BOTH - Different use cases (growth vs authenticity)

### nano-banana Requirements

The nano-banana skill uses Gemini 3 Pro for AI image generation. May require:
- `GOOGLE_API_KEY` environment variable in Railway
- Additional setup if Gemini API not already configured

### brand-voice-generator Output Location

This skill creates brand files at:
```
.claude/skills/pptx-generator/brands/{brand-name}/
```

This is intentional - brands created by this skill are designed for pptx-generator integration.

### Final Marketing Suite (17 Skills)

| Category | Skills |
|----------|--------|
| **Brand Foundation** | brand-voice, brand-voice-generator |
| **Social Media** | linkedin-viral, linkedin-post, x-post |
| **Long-form** | seo-content, geo-content, direct-response-copy |
| **Visual/Media** | landing-page-architecture, pptx-generator, excalidraw-diagram, base44-video, remotion, nano-banana |
| **Operations** | sop-creator, skill-creator, marketing-ideas |
