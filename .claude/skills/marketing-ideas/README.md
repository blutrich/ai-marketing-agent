# Marketing Ideas Skill for Claude Code

An interactive marketing brainstorm partner with **77 proven tactics** for Claude Code. Analyzes your content and suggests specific, actionable marketing ideas.

> "Every tactic here has one thing in common: AI can't do any of them."

## What is This?

A skill (plugin) for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) - Anthropic's official CLI tool. When you run `/marketing-ideas`, Claude becomes an interactive marketing consultant that:

1. Asks about your content (blog post, product launch, feature, event)
2. Asks about your goal (leads, buzz, sharing, competitive edge, etc.)
3. Matches your content to relevant tactics from a 77-tactic playbook
4. Gives you **specific, actionable suggestions** - not generic advice

## Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed
- A Claude API key or Claude Pro subscription

## Installation

```bash
# Clone to your Claude Code skills folder
git clone https://github.com/blutrich/marketing-ideas-skill.git ~/.claude/skills/marketing-ideas
```

That's it. The skill is now available.

## How to Use

### Step 1: Start the Skill

In your terminal, open Claude Code and type:

```
/marketing-ideas
```

### Step 2: Share Your Content

Claude will ask:
> "What content do you want to amplify?"

Share anything:
- A blog post or article
- A feature announcement
- A product launch
- An event you're planning
- Or just describe what you're working on

**Example:**
```
We just launched AI-powered meeting transcription for our app
```

### Step 3: Choose Your Goal

Claude will ask your primary goal:

| Goal | What It Means |
|------|---------------|
| **More leads/signups** | Convert attention into action |
| **Buzz without paid ads** | Organic virality and earned media |
| **Get customers to share** | Turn users into advocates |
| **Beat competitors** | Positioning and differentiation |
| **Retain customers** | Reduce churn, increase engagement |
| **Win at events** | Maximize conference/booth ROI |
| **Build for the future** | AI-proof, long-term channels |

### Step 4: Get Specific Ideas

Claude outputs 3-5 tactics tailored to YOUR content:

```
Based on your AI meeting transcription launch, here are 5 tactics to generate buzz:

🎸 **Create phone hotlines people can call**
Set up a demo line where people call in, say "transcribe this,"
and get their words transcribed in real-time. The call IS the demo.
Like Bland's billboard - 5% conversion rate.

🧸 **Build "the world's first meeting transcriber for [niche]"**
Create a landing page: "The first meeting transcriber for
stand-up comedians" or "for therapists" - absurdly specific = viral.

🎭 **Give your whole team fake job titles**
Have everyone update LinkedIn to "Chief Transcription Officer"
on launch day. 50 people = 50 job change notifications.
```

### Step 5: Go Deeper (Optional)

After initial suggestions, you can ask Claude to:
- Dive deeper into any tactic
- Build a LinkedIn content strategy (`linkedin-playbook.md`)
- Plan a Product Hunt launch (`product-hunt-playbook.md`)
- Brainstorm using the I.D.E.A. framework (`idea-framework.md`)
- Explore guerrilla tactics (`guerrilla-playbook.md`)

## Example Use Cases

### Product Launch
```
You: /marketing-ideas
You: "Launching a new design tool for developers next month"
Goal: Buzz without paid ads

Claude suggests: Reddit loophole posts, fake job title blast,
impossible feature announcement, countdown campaign...
```

### Growing LinkedIn Following
```
You: /marketing-ideas
You: "I write about AI tools and building products on LinkedIn"
Goal: More followers/reach

Claude suggests: One Big Idea positioning, carousel framework,
praise-led marketing, screenshot marketing...
```

### Event Promotion
```
You: /marketing-ideas
You: "We're hosting a booth at TechCrunch Disrupt"
Goal: Win at events

Claude suggests: Anti-booth booth strategy, counter-conference dinner,
pre-event outreach protocol, physical pattern interrupts...
```

### Competitor Crisis
```
You: /marketing-ideas
You: "Our main competitor just had a major outage"
Goal: Beat competitors

Claude suggests: Competitor Crisis Hero (help don't sell),
Google dorking for leads, comparison page SEO...
```

## What's Included

| File | Contents |
|------|----------|
| `SKILL.md` | Main skill with intake flow and brainstorming logic |
| `playbook.md` | 77 tactics organized by goal |
| `linkedin-playbook.md` | LinkedIn mastery: One Big Idea, employee advocacy, founder marketing |
| `idea-framework.md` | I.D.E.A. framework (Identify → Decode → Extract → Apply) + ICE scoring |
| `product-hunt-playbook.md` | 8-week Product Hunt dominance protocol |
| `guerrilla-playbook.md` | Pattern interrupts, event hijacking, Moonshot philosophy |

## All 77 Tactics (Categories)

### Leads & Conversions (12)
Waitlist upgrades, curiosity gaps, Baby Reindeer emails, brute-force gifts, hidden coupons, decoy pricing, calculators, phone hotlines...

### Buzz & Virality (15)
Impossible features, accidental emails, newsjacking, mini-games, fake job titles, billboard screenshots, niche landing pages...

### Customer Sharing (8)
Status symbols, customer spotlights, shareable results, progress celebrations, referral upgrades, team features...

### Competitive Edge (6)
Google dorking, ad library spying, comparison pages, category creation, anti-positioning...

### Retention (8)
Surprise upgrades, win-back sequences, milestone gifts, community loops, feedback features...

### Events (5)
Anti-booth booth, hallway hustle, pre-event lists, counter-events, physical pattern interrupts...

### Future-Proofing (8)
Personal brand moat, owned community, human touch points, relationship-first outreach, expertise moat...

### Engineering-as-Marketing (8)
Free tools, data products, widgets, APIs, template libraries, integrations, open source, interactive demos...

### Reddit Marketing (4)
The loophole (results without explanation), native ad formats (TIFU/AITAH), stealth brand flex, platform early mover...

### Crisis Response (3)
Crisis communication template, competitor crisis hero, anti-opportunistic play...

## Philosophy

This skill emphasizes tactics that:
- Require human creativity and judgment
- Need physical presence or real relationships
- Create pattern interrupts that feel authentic
- Can be executed in 24 hours
- Have asymmetric ROI (small effort, big impact)

## Sources

- Original marketing playbook (37 tactics)
- *Marketing Moonshots* by Tom Orbach
- Ongoing additions from Tom's newsletter

## Updating

To get the latest tactics:

```bash
cd ~/.claude/skills/marketing-ideas
git pull
```

## Contributing

PRs welcome! Add new tactics following the format in `playbook.md`:

```markdown
### [Number]. [Tactic Name]
**One-liner:** [Quick summary]
**How it works:** [Detailed explanation]
**Examples:** [Real companies]
**Best for:** [Content types]
**Psychology:** [Why it works]
```

## License

MIT - Use freely, credit appreciated.

---

Built for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) by [@blutrich](https://github.com/blutrich)
