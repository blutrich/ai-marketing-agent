# Product Requirements Document: AI Marketing System for Base44

## Executive Summary

**AI Marketing System** is a hybrid content generation and automation platform that combines Claude Agent SDK for high-quality content creation with platform-agnostic workflow orchestration (n8n, Make, or similar). The system enables Base44's marketing team to produce consistent, on-brand content at scale while automating distribution and lead management.

**MVP Goal:** Enable the marketing team to generate high-quality, voice-consistent content through AI skills, with automated workflows for scraping, scheduling, and distribution.

---

## Mission

Build a production-ready AI marketing system that replicates and extends The Boring Marketer's approach: capturing marketing expertise in reusable skills that produce ready-to-publish content with consistent brand voice.

### Core Principles

1. **Voice Control** - Content sounds like Ofer, not generic AI
2. **Expertise Capture** - Skills encode marketing knowledge, not just instructions
3. **Flow, Not Friction** - Output ready content, not drafts to fix
4. **Layered Architecture** - Strategy → Execution → Platform → Distribution
5. **Hybrid Automation** - Best tool for each job (Claude for quality, orchestrator for automation)

---

## Target Users

### Primary Users

**Marketing Team Members** who need to:
- Generate LinkedIn posts, emails, and blog content
- Maintain consistent brand voice across all channels
- Repurpose content across multiple platforms
- Track competitor activity and industry trends

**Technical Comfort Level:** Comfortable using chat interfaces and no-code tools; developers handle Claude Agent SDK integration.

### Secondary Users

**Developers/Technical Staff** who:
- Set up and maintain the Claude Agent SDK endpoint
- Configure webhook integrations between Gumloop and Claude
- Manage skills library and version control

---

## System Architecture

### Hybrid Architecture Decision

| Component | Platform | Rationale |
|-----------|----------|-----------|
| **Website** | Wix (Base44) | Existing platform |
| **Orchestration** | Any webhook-capable platform | No vendor lock-in |
| **Content Engine** | Claude Agent SDK | Best quality, skills auto-loaded |
| **Deployment** | Railway | Zero maintenance, auto-deploy |
| **Frontend** | Orchestrator UI + Google Sheets | No custom UI needed |

### Orchestration Platform Options (No Vendor Lock-in)

The system uses **standard webhooks** for all integrations, making it portable across platforms:

| Platform | Cost | Strengths | Best For |
|----------|------|-----------|----------|
| **Base44 Web App** | Included | Native integration, full control, custom UI | Best integration, dogfooding |
| **n8n** | Free (self-host) / $20/mo (cloud) | Open-source, self-hostable, 400+ nodes | Quick start, privacy |
| **Make** | $9-16/mo | Visual builder, 1000+ apps | Non-technical teams |
| **Gumloop** | $0-97/mo | AI-native, built-in scraping | AI-focused workflows |
| **Zapier** | $20-50/mo | Largest app ecosystem | Simple automations |

**Why no lock-in:**
- Claude endpoint uses **standard HTTP webhooks** (POST JSON)
- Any platform that can send HTTP requests works
- No proprietary SDK or APIs required
- Workflows are conceptual (scrape → generate → post) - implementable anywhere

**Recommended:**
- **Long-term:** Build into Base44 web app for native experience
- **Quick start:** n8n (self-hosted) or Make for rapid prototyping

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│       ORCHESTRATOR (Base44 App / n8n / Make / Zapier)       │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │ Trigger  │───▶│ Scrape   │───▶│ Webhook  │──────────┐   │
│  │ (cron/   │    │ Data     │    │ POST     │          │   │
│  │  manual) │    │          │    │          │          │   │
│  └──────────┘    └──────────┘    └──────────┘          │   │
│                                                         │   │
│  ┌──────────┐    ┌──────────┐                          │   │
│  │ Post to  │◀───│ Receive  │◀─────────────────────────┘   │
│  │ LinkedIn │    │ Response │   (synchronous response)     │
│  └──────────┘    └──────────┘                              │
└─────────────────────────────────────────────────────────────┘
                           │
              Standard HTTP POST (JSON)
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              CLAUDE AGENT SDK (Content Engine)              │
│                                                             │
│  Skills auto-loaded from: .claude/skills/SKILL.md          │
│                                                             │
│  Webhook API:                                               │
│  POST /generate                                             │
│  {                                                          │
│    "prompt": "Create LinkedIn post about...",               │
│    "skills": ["brand-voice", "linkedin-viral"],             │
│    "context": { ... }                                       │
│  }                                                          │
│                                                             │
│  Deploy: Railway ($5-10/mo) - zero maintenance             │
└─────────────────────────────────────────────────────────────┘
```

### Skills Architecture (Layered System)

```
┌─────────────────────────────────────────────────────────────┐
│                    STRATEGY LAYER                           │
│  marketing-ideas skill (77 tactics, 5 playbooks) [GLOBAL]  │
│  → WHAT to create: tactics, campaigns, approaches          │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    EXECUTION LAYER                          │
│  direct-response-copy → THE SLIDE framework                │
│  seo-content → Traditional SEO optimization                │
│  geo-content → AI citation optimization                    │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    PLATFORM LAYER                           │
│  linkedin-viral → Hook patterns, carousels, algorithm      │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   FOUNDATION LAYER                          │
│  brand-voice → Applied LAST to all content (tone, voice)   │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│            DISTRIBUTION LAYER (n8n / Make / etc.)           │
│  → Schedule posts, track performance, scrape competitors   │
└─────────────────────────────────────────────────────────────┘
```

---

## MVP Scope

### In Scope

**Skills Library (Phase 1): COMPLETE**
- [x] `brand-voice` - Foundation skill for consistent tone
- [x] `marketing-ideas` - 77 tactics across 5 playbooks (global skill)
- [x] `direct-response-copy` - THE SLIDE conversion framework
- [x] `linkedin-viral` - Hook patterns and formats
- [x] `seo-content` - Traditional SEO optimization
- [x] `geo-content` - AI citation optimization (GEO)

**Automation Workflows (Phase 2) - Platform Agnostic:**
- [ ] Competitor scraping workflow (LinkedIn posts)
- [ ] Webhook trigger to Claude endpoint
- [ ] LinkedIn posting workflow
- [ ] Google Sheets logging

*Implementable on: n8n, Make, Gumloop, or Zapier*

**Integration (Phase 3):**
- [ ] Claude Agent SDK endpoint (FastAPI/Express)
- [ ] Webhook connection (standard HTTP POST)
- [ ] End-to-end workflow testing

### Out of Scope (Future Considerations)

- Custom web UI (use orchestrator UI + Sheets)
- Real-time chat interface
- Multi-tenant support
- Advanced analytics dashboard
- Video content generation
- Email sequence automation (Phase 4+)
- Lead enrichment workflows (Phase 4+)

---

## User Stories

### Content Creation

1. **As a marketer, I want to generate LinkedIn posts in Ofer's voice**, so that content sounds authentic and on-brand.
   - Input: Topic or idea
   - Output: Ready-to-post LinkedIn content with hook, body, CTA

2. **As a marketer, I want to get marketing tactic suggestions**, so that I can plan effective campaigns.
   - Input: Goal (leads, buzz, retention)
   - Output: Relevant tactics from the 77-tactic playbook

3. **As a marketer, I want to convert features into benefits**, so that copy resonates emotionally.
   - Input: Product feature
   - Output: Benefit-focused copy using THE SLIDE framework

### Automation

4. **As a marketer, I want to automatically scrape competitor posts**, so that I can learn from successful content.
   - Trigger: Daily cron job
   - Output: Competitor posts saved to database/sheet

5. **As a marketer, I want to schedule posts automatically**, so that content publishes at optimal times.
   - Input: Generated content
   - Output: Scheduled LinkedIn post

6. **As a marketer, I want all content logged**, so that I can track what was published.
   - Trigger: Post published
   - Output: Row added to Google Sheets with date, content, platform

---

## Skills Specification

### Skill 1: `brand-voice` (Foundation)

**Purpose:** Ensure all content sounds like Ofer Blutrich

**Key Components:**
- BASE44 Voice Framework (Be specific, Acknowledge limitations, Short sentences, Emotional core, 4th grade reading, 4 truths)
- Kill List (words to never use)
- Add List (patterns to use often)
- Quality checklist

**Auto-invoke:** All content generation tasks

**Depends on:** None (foundation)
**Used by:** All other skills

---

### Skill 2: `marketing-ideas` (Strategy)

**Purpose:** Provide tactical marketing suggestions

**Playbooks:**
1. `playbook.md` - Main 77 tactics (leads, buzz, retention, events, AI-proof)
2. `linkedin-playbook.md` - LinkedIn mastery (founder marketing 40/30/20/10)
3. `guerrilla-playbook.md` - High-impact, low-budget tactics
4. `product-hunt-playbook.md` - 8-week launch protocol
5. `idea-framework.md` - I.D.E.A. systematic creativity

**Auto-invoke:** Campaign planning, content ideation

---

### Skill 3: `direct-response-copy` (Execution)

**Purpose:** Write copy that converts

**THE SLIDE Framework:**
```
S - Situation (set the scene)
L - Limitation (what's holding them back)
I - Implication (cost of not acting)
D - Destination (where they want to be)
E - Evidence (proof it works)
```

**SO WHAT Chain:**
```
Feature → Functional → Financial → Emotional
                                   ↑
                            START HERE
```

**Auto-invoke:** Landing pages, ads, sales emails

---

### Skill 4: `linkedin-viral` (Platform)

**Purpose:** Optimize content for LinkedIn algorithm

**Components:**
- Hook templates (10+ patterns)
- Post structures (story, listicle, carousel)
- CTA patterns
- Algorithm optimization rules
- Engagement triggers

**Auto-invoke:** LinkedIn post generation

---

### Skill 5: `seo-content` (Discovery - Traditional)

**Purpose:** Rank on Google search

**Content Types:**
| Type | Length | Purpose |
|------|--------|---------|
| Pillar Guide | 5-8K words | Authority |
| How-To | 2-3K words | Traffic |
| Comparison | 2.5-4K words | Bottom-funnel |
| Listicle | 2-3K words | Shareability |

**Auto-invoke:** Blog posts, guides, articles

---

### Skill 6: `geo-content` (Discovery - AI)

**Purpose:** Get cited by AI systems (ChatGPT, Perplexity, Claude)

**Content Types:**
| Type | Length | Purpose |
|------|--------|---------|
| Definition Page | 500-1K words | Quick answers |
| Data/Research | 1-2K words | Citeable stats |
| Expert Take | 800-1.5K words | Opinions |
| Structured FAQ | 1-2K words | Direct answers |

**Win Condition:** "According to [Base44]..." in AI responses

**Auto-invoke:** Authority content, research pieces

---

## Technology Stack

### Content Engine

- **Claude Agent SDK** - Python or TypeScript
- **Claude claude-sonnet-4-20250514** - Primary model
- **FastAPI/Express** - Webhook endpoint
- **Docker** - Containerization

### Orchestration (Choose One)

| Platform | Pricing | Notes |
|----------|---------|-------|
| **Base44 Web App** | Included | Best long-term - native integration |
| **n8n** | Free (self-host) / $20/mo cloud | Quick start - open source |
| **Make** | $9/mo (Core) / $16/mo (Pro) | Great UI, 1000+ apps |
| **Gumloop** | Free tier / $97/mo Pro | AI-native features |
| **Zapier** | $20/mo (Starter) | Largest ecosystem |

### Storage

- **Google Sheets** - Content log, tracking
- **Platform Database** - Workflow data (n8n: SQLite/Postgres, Make: built-in, etc.)

### Deployment: Railway (Recommended)

**Why Railway:**
- Zero server maintenance (no SSH, no Linux, no security updates)
- Auto-deploy on git push
- Built-in monitoring and logs
- Scales automatically
- ~$5-10/mo for typical usage

**Setup:**
1. Connect GitHub repo
2. Add `ANTHROPIC_API_KEY` environment variable
3. Done - deploys automatically

**Alternatives (if needed):**
| Platform | Cost | Notes |
|----------|------|-------|
| Render | $7/mo | Similar simplicity |
| Fly.io | $5/mo | Edge deployment |
| VPS (Hostinger/DO) | $5-6/mo | More control, more maintenance |

---

## Directory Structure

```
# PROJECT SKILLS (this repo)
.claude/skills/                    # Project-specific skills
├── brand-voice/
│   └── SKILL.md                   # Foundation voice skill
├── direct-response-copy/
│   └── SKILL.md                   # THE SLIDE framework
├── linkedin-viral/
│   └── SKILL.md                   # Hook patterns, formats
├── seo-content/
│   └── SKILL.md                   # Traditional SEO
└── geo-content/
    └── SKILL.md                   # AI citation optimization

# GLOBAL SKILL (user's home directory)
~/.claude/skills/                  # Global skills (shared across projects)
└── marketing-ideas/               # 77 tactics, 5 playbooks
    ├── SKILL.md                   # Main skill definition
    ├── playbook.md                # 77 tactics
    ├── linkedin-playbook.md       # LinkedIn mastery
    ├── guerrilla-playbook.md      # Guerrilla tactics
    ├── product-hunt-playbook.md   # PH launch protocol
    └── idea-framework.md          # I.D.E.A. framework

# DOCUMENTATION
.agents/                           # Documentation & templates
├── AI-Marketing-System-PRD.md     # This document
├── reference/
│   └── ai-marketing-system-architecture.md
└── skills/
    ├── _template/skill-template.md
    └── brand-voice/skill.md       # Original template

# WEBHOOK SERVER (to create)
server/                            # Claude Agent SDK endpoint
├── main.py                        # FastAPI app
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

**Note:** `marketing-ideas` is a global skill available across all projects.
Project skills in `.claude/skills/` are specific to this marketing system.

---

## Implementation Phases

### Phase 1: Skills Library (Week 1-2) - COMPLETE
**Goal:** Complete skills for content generation

**Deliverables:**
- [x] `brand-voice/SKILL.md` - Foundation skill
- [x] `marketing-ideas/` - Full playbook structure (global skill)
- [x] `direct-response-copy/SKILL.md` - THE SLIDE framework
- [x] `linkedin-viral/SKILL.md` - Hook patterns
- [x] `seo-content/SKILL.md` - SEO optimization
- [x] `geo-content/SKILL.md` - AI citation

**Validation:** Claude generates on-brand content using skills

---

### Phase 2: Automation Setup (Week 2-3)
**Goal:** Automation workflows operational

**Platform Options:** Base44 Web App, n8n, Make, Gumloop, or Zapier

**Deliverables:**
- [ ] Orchestration platform setup
- [ ] Competitor scraping workflow
- [ ] Webhook trigger workflow
- [ ] LinkedIn posting workflow
- [ ] Google Sheets logging

**Validation:** Can scrape competitors and log to Sheets

**Platform-Specific Setup:**

| Platform | Setup Notes |
|----------|-------------|
| **Base44 Web App** | Build webhook triggers and scheduling into the app |
| **n8n** | Self-host with Docker, or use n8n.cloud |
| **Make** | Sign up at make.com, use HTTP module for webhooks |
| **Gumloop** | Sign up at gumloop.com, native AI features |
| **Zapier** | Sign up at zapier.com, use Webhooks by Zapier |

---

### Phase 3: Integration (Week 3-4)
**Goal:** End-to-end workflow operational

**Deliverables:**
- [ ] Claude Agent SDK endpoint deployed
- [ ] Webhook integration tested
- [ ] Full workflow: scrape → generate → post
- [ ] Error handling and retry logic

**Validation:** Automated daily content generation working

---

### Phase 4: Expansion (Week 4+)
**Goal:** Additional workflows

**Potential Additions:**
- [ ] Lead enrichment (CRM integration)
- [ ] Email sequence automation
- [ ] Content atomization (1 article → 10 posts)
- [ ] Performance tracking feedback loop

---

## Example Workflow

**Automated Daily LinkedIn Post:**

```
1. Orchestrator: Cron trigger (daily 9am)
2. Orchestrator: Scrape competitor LinkedIn posts
3. Orchestrator: Send data via webhook to Claude endpoint
4. Claude: Use marketing-ideas skill → select tactic for today
5. Claude: Use linkedin-viral skill → format for platform
6. Claude: Use brand-voice skill → apply voice/tone
7. Claude: Return content via webhook
8. Orchestrator: Receive content
9. Orchestrator: Schedule post to LinkedIn
10. Orchestrator: Log to Google Sheets
```

*Works identically on n8n, Make, Gumloop, or Zapier*

**Skills Chain:**
```
User: "Create LinkedIn content for our AI consulting launch"

1. marketing-ideas skill activates:
   → Suggests "Praise-Led Marketing" tactic
   → Recommends "Founder Marketing 40/30/20/10 mix"

2. linkedin-viral skill applies:
   → Formats as carousel with hook
   → Adds algorithm-friendly structure

3. brand-voice skill finalizes:
   → Applies Ofer's specific tone
   → Removes kill-list words
   → Ensures authenticity
```

---

## Success Criteria

### Content Quality
- [ ] Generated content passes brand voice checklist
- [ ] Zero kill-list words in output
- [ ] At least 3 specific numbers/examples per piece
- [ ] Reads naturally when spoken aloud

### Automation Reliability
- [ ] Daily workflow completes without manual intervention
- [ ] Webhook responses under 30 seconds
- [ ] Error handling catches and reports failures
- [ ] All content logged to tracking sheet

### Business Impact
- [ ] LinkedIn followers: +100/week
- [ ] Post impressions: 10K+ average
- [ ] Content production: 5x faster than manual
- [ ] Brand consistency: 100% on-voice

---

## Verification Checklist

### Phase 1 Complete When: DONE
- [x] All 6 skills created and documented
- [x] Brand-voice skill produces authentic content
- [x] Marketing-ideas provides relevant tactics (global skill)
- [x] Skills work together (layered approach)

### Phase 2 Complete When:
- [ ] Orchestrator scrapes competitor content successfully
- [ ] Webhooks trigger correctly
- [ ] LinkedIn posting works
- [ ] Google Sheets logging works

### Phase 3 Complete When:
- [ ] Full workflow runs end-to-end
- [ ] Content quality meets standards
- [ ] No manual intervention required
- [ ] Errors handled gracefully

---

## Risks & Mitigations

### Risk: Content Quality Inconsistency
**Mitigation:** Strong brand-voice skill with kill list and quality checklist

### Risk: Orchestration Platform Limitations
**Mitigation:** Platform-agnostic webhook design - switch platforms anytime without code changes

### Risk: API Rate Limits
**Mitigation:** Batch processing, retry logic, queue management

### Risk: Webhook Timeouts
**Mitigation:** Async processing, background jobs for long content

### Risk: Platform API Changes
**Mitigation:** Orchestration layer handles platform integration, abstracts changes

---

## Cost Estimate

### Monthly Costs

| Item | Cost (Min) | Cost (Max) | Notes |
|------|------------|------------|-------|
| **Wix (Base44)** | Existing | Existing | Already paid |
| **Railway** | $5 | $10 | Agent hosting |
| **Orchestration** | $0 | $20 | n8n free, Make $9-16 |
| **Claude API** | ~$20 | ~$50 | Depends on volume |
| **Total** | **~$25/mo** | **~$80/mo** | Scales with usage |

**Cost by Orchestration Choice:**

| Setup | Monthly Cost |
|-------|--------------|
| n8n (self-host) + Railway | ~$25-60 |
| n8n (cloud) + Railway | ~$45-80 |
| Make + Railway | ~$35-75 |
| Zapier + Railway | ~$45-80 |

### Comparison to Alternatives

| Approach | Monthly Cost | Setup Time |
|----------|--------------|------------|
| Manual content creation | $2,000+ (time) | N/A |
| Agency | $3,000-10,000 | 2-4 weeks |
| This system | $25-80 | 2-4 weeks |

---

## Appendix

### Related Documents
- [AI Marketing System Architecture](./reference/ai-marketing-system-architecture.md)
- [Skill Template](./skills/_template/skill-template.md)
- [Brand Voice Skill](./skills/brand-voice/skill.md)

### Key References
- The Boring Marketer's frameworks
- Claude Agent SDK documentation
- n8n documentation (https://docs.n8n.io)
- Make documentation (https://www.make.com/en/help)
- Gary Halbert letters (copywriting)
- Eugene Schwartz "Breakthrough Advertising"

### Platform URLs

**Orchestration (choose one):**
- n8n: https://n8n.io (recommended)
- Make: https://make.com
- Gumloop: https://gumloop.com
- Zapier: https://zapier.com

**Content Engine:**
- Claude Agent SDK: https://docs.anthropic.com/en/docs/agents-and-tools/claude-agent-sdk

**Agent Hosting:**
- Railway: https://railway.app (recommended)
- Render: https://render.com (alternative)

**Website:**
- Wix: https://wix.com (Base44 current platform)

---

*Last updated: 2025-01-19*
*Version: 1.0*
