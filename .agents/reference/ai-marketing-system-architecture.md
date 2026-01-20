# AI Marketing System Architecture
## Reverse-Engineered from The Boring Marketer

**Goal:** Build a complete AI marketing system for Base44 that replicates and extends The Boring Marketer's approach.

---

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    AI MARKETING SYSTEM                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │   RESEARCH  │───▶│   CREATE    │───▶│  DISTRIBUTE │         │
│  │    LAYER    │    │    LAYER    │    │    LAYER    │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
│        │                  │                  │                  │
│        ▼                  ▼                  ▼                  │
│  ┌───────────────────────────────────────────────────┐         │
│  │              SKILLS LIBRARY                        │         │
│  │  ┌─────────┬─────────┬─────────┬─────────┐        │         │
│  │  │brand-   │content- │direct-  │seo-     │        │         │
│  │  │voice    │atomizer │response │content  │        │         │
│  │  ├─────────┼─────────┼─────────┼─────────┤        │         │
│  │  │lead-    │email-   │linkedin-│ad-      │        │         │
│  │  │magnet   │sequence │viral    │creative │        │         │
│  │  └─────────┴─────────┴─────────┴─────────┘        │         │
│  └───────────────────────────────────────────────────┘         │
│                          │                                      │
│                          ▼                                      │
│  ┌───────────────────────────────────────────────────┐         │
│  │              TOOLS & MCP SERVERS                   │         │
│  │  Playwright | Perplexity | Firecrawl | Apify      │         │
│  │  Image Gen  | Video Gen  | Analytics | CRM        │         │
│  └───────────────────────────────────────────────────┘         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component 1: Skills Library

Based on The Boring Marketer's 10-step skill creation process.

### Core Skills (Priority Order)

#### 1. `brand-voice` - Foundation Skill
**Purpose:** Establish consistent voice across all content

**Structure:**
```markdown
# Brand Voice Skill

## Identity
- Who: [Your positioning]
- Voice: "Smart friend who figured something out"
- Tone: Conversational, specific, emotional

## Voice Principles
1. Specificity over vagueness: "$47,329" not "lots of money"
2. Rhythm: Short. Then breathe. Land it.
3. Write from emotion (end of the SO WHAT chain)

## Kill List (Words to avoid)
- "delve", "comprehensive", "landscape"
- "in today's world", "robust", "streamline"
- "leverage", "synergy", "cutting-edge"

## Add List (Patterns to use)
- Specific numbers and dates
- Real examples with names
- Personal opinions and hot takes
- Acknowledged limitations

## Voice Test
"Would I say this out loud to a smart friend?"
```

#### 2. `direct-response-copy` - Conversion Skill
**Purpose:** Write copy that converts

**The SLIDE Framework:**
```
1. Headline     → 80% of the work
2. Problem      → Quantify it ("87% of marketers...")
3. Agitate      → Make vivid (paint the pain)
4. Credibility  → Why listen to you?
5. Solution     → Transform (before → after)
6. Proof        → Specific ("helped 2,894 makers")
7. CTA          → Benefit-focused ("Get the system")
```

**SO WHAT Chain:**
```
Feature → Functional → Financial → Emotional
                                   ↑
                            START HERE
```

#### 3. `content-atomizer` - Distribution Skill
**Purpose:** Turn one piece into many

**Atomization Matrix:**
```
Long-form Article (3000 words)
    ↓
├── LinkedIn post (hook + 3 bullets)
├── Twitter thread (8-12 tweets)
├── Email newsletter section
├── 3x short-form video scripts
├── 10x quote graphics
├── Carousel (8-10 slides)
└── Audio/podcast segment
```

#### 4. `linkedin-viral` - Platform Skill
**Purpose:** Reverse-engineer LinkedIn virality

**6-Step System:**
1. NICHE ID → Find top 10 creators in AI consulting
2. SCRAPE → 900+ posts via Apify
3. ANALYZE → Extract patterns (hooks, formats, CTAs)
4. PLAYBOOK → Codify what works
5. LAYER VOICE → Apply brand-voice skill
6. CONVERT → Execute with proven patterns

**Hook Templates:**
```
- "I [unexpected action] and here's what happened..."
- "[Number] [things] I wish I knew about [topic]"
- "Stop [common action]. Do [better action] instead."
- "The [topic] playbook nobody talks about:"
- "[Controversial opinion] (here's why)"
```

#### 5. `seo-content` - Discovery Skill (Traditional SEO)
**Purpose:** Rank on Google

**Content Types & Lengths:**
| Type | Length | Purpose |
|------|--------|---------|
| Pillar Guide | 5-8K words | Authority |
| How-To | 2-3K words | Traffic |
| Comparison | 2.5-4K words | Bottom-funnel |
| Listicle | 2-3K words | Shareability |

**Structure:**
- Keyword in title, H1, H2s
- Match Featured Snippet format
- FAQ section (schema-ready)
- Answer intent completely

#### 6. `geo-content` - AI Discovery Skill (NEW)
**Purpose:** Get cited by AI (ChatGPT, Perplexity, Claude)

**Content Types & Lengths:**
| Type | Length | Purpose |
|------|--------|---------|
| Definition Page | 500-1K words | Quick answers |
| Data/Research | 1-2K words | Citeable stats |
| Expert Take | 800-1.5K words | Opinions |
| Structured FAQ | 1-2K words | Direct answers |

**Structure:**
- Concise, definitive statements
- Quotable paragraphs (standalone value)
- One clear answer per question
- Stats in cite-ready format

**Win Condition:** "According to [you]..." in AI responses

#### 7. `email-sequences` - Nurture Skill
**Purpose:** Convert subscribers to customers

**Core Sequences:**
1. Welcome (5 emails)
2. Nurture (ongoing weekly)
3. Launch (7-day campaign)
4. Re-engagement (3 emails)

#### 8. `lead-magnet` - Acquisition Skill
**Purpose:** Trade value for email

**High-Converting Formats:**
- Checklists (quick win)
- Templates (immediate use)
- Swipe files (inspiration)
- Mini-courses (education)
- Calculators (personalized value)

#### 9. `ad-creative` - Paid Skill
**Purpose:** Generate high-converting ad creatives

**Process (from Ad Agent demo):**
1. Find competitors
2. Learn from their ads
3. Generate on-brand creatives
4. Package in report

#### 10. `orchestrator` - Meta Skill
**Purpose:** Coordinate other skills

```
GOAL: "Create launch campaign for [product]"
    ↓
ORCHESTRATOR decides:
├── lead-magnet skill → Create opt-in
├── email-sequences skill → Write launch sequence
├── linkedin-viral skill → Create 5 posts
├── ad-creative skill → Generate ad variants
└── content-atomizer skill → Repurpose everything
```

---

## Component 2: Agent Architecture

Based on Claude Agent SDK patterns.

### Agent Loop
```
GOAL: "[Marketing objective]"
        ↓
AGENT LOOP: observe → think → act → learn → repeat
        ↓
┌───────────────┬───────────────┬─────────────────┐
│  SUBAGENTS    │   SKILLS      │    TOOLS        │
│───────────────│───────────────│─────────────────│
│ researcher    │ brand-voice   │ Built-in:       │
│ writer        │ direct-resp.  │ Read, Write,    │
│ editor        │ linkedin-viral│ Bash, Grep      │
│ analyst       │ seo-content   │                 │
│               │ geo-content   │ MCP:            │
│ (parallel,    │ email-seq     │ Playwright,     │
│  isolated)    │               │ Perplexity,     │
│               │ (auto-invoked │ Firecrawl,      │
│               │  by domain)   │ Apify           │
└───────────────┴───────────────┴─────────────────┘
        ↓
HOOKS: brand guidelines, compliance, human-review
        ↓
STRUCTURED OUTPUT: JSON matching content schema
```

### Subagent Definitions

#### `researcher`
- Competitive analysis
- Trend identification
- Audience research
- Content gap analysis

#### `writer`
- Draft creation
- Content generation
- Copy variations

#### `editor`
- Quality review
- Brand compliance
- Tone adjustment
- Fact-checking

#### `analyst`
- Performance tracking
- Pattern extraction
- Optimization recommendations

---

## Component 3: AI Creative Stack

For visual content generation.

```
┌─────────────────────────────────────────────────┐
│           AI CREATIVE STRATEGIST                │
│  Research → Preview (2-3) → Feedback → Brief    │
└─────────────────────────────────────────────────┘
                    ↓
    ┌───────────────┼───────────────┐
    ↓               ↓               ↓
┌─────────┐   ┌─────────┐   ┌─────────┐
│Product  │   │Social   │   │General  │
│Photos   │   │Graphics │   │Images   │
└─────────┘   └─────────┘   └─────────┘
    │               │               │
    └───────────────┼───────────────┘
                    ↓
        ┌─────────────────────┐
        │   NANO BANANA PRO   │
        │      (~3 min)       │
        └─────────────────────┘
                    ↓
    ┌───────────────┼───────────────┐
    ↓               ↓               ↓
┌─────────┐   ┌─────────┐   ┌─────────┐
│SORA 2   │   │VEO 3.1  │   │KLING    │
│~80s     │   │~130s    │   │v2.5     │
└─────────┘   └─────────┘   │~155s    │
                            └─────────┘
                    ↓
        ┌─────────────────────┐
        │  USER PICKS BEST    │
        └─────────────────────┘
                    ↓
        ┌─────────────────────┐
        │  KLING LIP-SYNC     │
        │  (+ speech/avatar)  │
        └─────────────────────┘
```

---

## Component 4: MCP Server Integrations

### Required MCPs

| MCP Server | Purpose | Use Case |
|------------|---------|----------|
| **Playwright** | Web automation | Scrape competitor content, visual inspiration |
| **Perplexity** | AI search | Research, trend analysis |
| **Firecrawl** | Web scraping | Extract content at scale |
| **Apify** | Social scraping | LinkedIn/Twitter post extraction |
| **Supabase** | Database | Store content, analytics, leads |
| **MongoDB** | Document store | Content library, templates |

### Optional MCPs

| MCP Server | Purpose |
|------------|---------|
| Buffer/Hootsuite | Social scheduling |
| Mailchimp/ConvertKit | Email automation |
| Google Analytics | Performance tracking |
| Ahrefs/SEMrush | SEO research |

---

## Component 5: Directory Structure

```
.agents/
├── skills/
│   ├── brand-voice/
│   │   ├── skill.md           # Skill definition
│   │   ├── examples/          # Good/bad examples
│   │   └── tests/             # Validation scenarios
│   ├── direct-response-copy/
│   ├── content-atomizer/
│   ├── linkedin-viral/
│   ├── seo-content/
│   ├── geo-content/
│   ├── email-sequences/
│   ├── lead-magnet/
│   ├── ad-creative/
│   └── orchestrator/
├── agents/
│   ├── researcher.md
│   ├── writer.md
│   ├── editor.md
│   └── analyst.md
├── workflows/
│   ├── content-campaign.md
│   ├── linkedin-growth.md
│   ├── seo-article.md
│   └── launch-sequence.md
├── templates/
│   ├── linkedin-hooks.md
│   ├── email-templates.md
│   ├── ad-frameworks.md
│   └── landing-page.md
└── playbooks/
    ├── competitor-analysis.md
    ├── content-calendar.md
    └── performance-review.md
```

---

## Implementation Phases

### Phase 1: Foundation (Week 1-2)
- [ ] Create `brand-voice` skill for Base44
- [ ] Create `direct-response-copy` skill
- [ ] Set up basic directory structure
- [ ] Document voice guidelines and kill list

### Phase 2: Content Skills (Week 3-4)
- [ ] Create `linkedin-viral` skill
- [ ] Create `seo-content` skill
- [ ] Create `geo-content` skill
- [ ] Build hook/template libraries

### Phase 3: Automation Skills (Week 5-6)
- [ ] Create `content-atomizer` skill
- [ ] Create `email-sequences` skill
- [ ] Create `lead-magnet` skill
- [ ] Set up MCP integrations (Playwright, Apify)

### Phase 4: Agent System (Week 7-8)
- [ ] Define subagent roles
- [ ] Create `orchestrator` skill
- [ ] Build workflow automations
- [ ] Implement hooks and guardrails

### Phase 5: Creative Stack (Week 9-10)
- [ ] Set up image generation pipeline
- [ ] Integrate video generation (SORA/VEO/KLING)
- [ ] Create `ad-creative` skill
- [ ] Build review/approval workflows

### Phase 6: Analytics & Optimization (Ongoing)
- [ ] Performance tracking setup
- [ ] A/B testing frameworks
- [ ] Pattern extraction automation
- [ ] Continuous skill improvement

---

## Success Metrics

### Content Performance
- LinkedIn: 100+ followers/week, 10K+ impressions/post
- SEO: Page 1 rankings for target keywords
- GEO: Cited in AI responses

### Efficiency Gains
- Content creation: 10x faster
- Consistency: 100% on-brand
- Distribution: Automated atomization

### Business Impact
- Lead generation: X leads/month
- Conversion: X% improvement
- Revenue: Attributable to content

---

## The 4 Core Truths (Applied to Base44)

| Truth | Application |
|-------|-------------|
| **Expertise Transfer** | Skills capture Ofer's consulting expertise, not just instructions |
| **Flow, Not Friction** | Output ready content, not intermediate drafts |
| **Voice Matches Domain** | Sound like an AI consultant, not generic marketing |
| **Focused Beats Comprehensive** | Each skill does one thing exceptionally well |

---

## Next Steps

1. **Define Base44's Brand Voice** - Core identity, positioning, tone
2. **Identify Top 10 Competitors** - For LinkedIn scraping/analysis
3. **Choose Priority Skills** - Which 3 skills to build first
4. **Set Up MCP Stack** - Playwright, Apify, Perplexity
5. **Create First Skill** - `brand-voice` as foundation

---

*This architecture is based on reverse-engineering The Boring Marketer's public content and adapting it for Base44's AI consulting practice.*
