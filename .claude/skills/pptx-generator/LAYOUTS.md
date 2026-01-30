# Layout Selection Guide

Detailed guidance for selecting and using layouts effectively.

## Layout Discovery (READ ALL FRONTMATTERS)

**⚠️ MANDATORY: Read ALL layout frontmatters before selecting any layout.**

### Step 1: Discover all layouts
```
Glob: .claude/skills/pptx-generator/cookbook/*.py
```

### Step 2: Read EVERY layout file (first 40 lines)

For each `.py` file, extract the `# /// layout` frontmatter block:

```python
# /// layout
# name = "floating-cards-slide"
# purpose = "Feature highlights, process steps, multiple equal items with depth"
# best_for = [
#     "Exactly 3 related features or concepts",
#     "Process with 3 steps",
# ]
# avoid_when = [
#     "More than 3 items - use multi-card-slide instead",
#     "Long card titles (over 15 characters)",
# ]
# max_cards = 3
# card_title_max_chars = 15
# ///
```

**Key frontmatter fields:**
| Field | Description |
|-------|-------------|
| `name` | Layout identifier |
| `purpose` | What this layout is for |
| `best_for` | Ideal use cases (array) |
| `avoid_when` | When NOT to use this layout (array) |
| `max_*` / `min_*` | Item limits |
| `instructions` | Specific tips |

### Step 3: Select layouts (only AFTER reading all)

1. User specifies layout → Use that layout (verify it fits)
2. User describes content → Match to `best_for` criteria
3. **Check `avoid_when`** → Don't use in warned situations
4. **Respect limits** → If content exceeds `max_*`, use different layout

---

## Visual-First Layout Selection (CRITICAL FOR VARIETY)

**🎨 DEFAULT TO VISUAL LAYOUTS. Content-slide is the LAST RESORT.**

### The Variety Problem

The biggest mistake is **defaulting to content-slide** (title + bullets). This creates repetitive presentations.

**Common failure pattern:**
- 11 out of 30 slides = content-slide (37% repetition)
- User says "this lacks variety"

### Variety Enforcement Rules

**HARD LIMITS:**
1. **Never use the same layout more than 2-3 times consecutively**
2. **Content-slide should be <25% of total slides**
3. **Visual layouts should be 50%+ of slides**
4. **Section breaks don't count toward variety**

### Decision Tree: "Should I Use content-slide?"

Ask IN ORDER before using content-slide:

```
Do I have 3-5 equal items?
  YES → Use multi-card-slide

Do I have 2-4 big numbers/metrics?
  YES → Use stats-slide

Am I comparing two things?
  YES → Use two-column-slide

Do I have a central concept with surrounding items?
  YES → Use circular-hero-slide

Do I have exactly 3 related items?
  YES → Use floating-cards-slide

Do I have 1-3 words to emphasize dramatically?
  YES → Use giant-focus-slide or bold-diagonal-slide

Do I have a powerful quote?
  YES → Use quote-slide

Is this the ONLY way to present this?
  YES → NOW use content-slide
```

---

## Transforming Bullets Into Visual Layouts

**Example 1: "Validation Patterns"**

❌ **BAD (content-slide):**
```
Title: Validation Patterns
Bullets:
- Run comprehensive test suites
- Type checking and linting
- Code review by humans and AI
```

✅ **GOOD (multi-card-slide):**
```
Cards:
1. Testing | Run comprehensive test suites
2. Linting | Type checking and formatting
3. Review | Human and AI code review
```

**Example 2: "Human-in-the-Loop Strategy"**

❌ **BAD (content-slide):**
```
Bullets:
- In-the-loop: Human approves before execution
- On-the-loop: Human reviews after completion
```

✅ **GOOD (two-column-slide):**
```
Left: In-the-Loop | Human approves before execution
Right: On-the-Loop | Human reviews after completion
```

---

## Quick Reference: Content Type → Best Layout

| Content Type | Best Layout |
|--------------|-------------|
| 3-5 equal features/steps | multi-card-slide |
| Exactly 3 featured items | floating-cards-slide |
| 2-4 metrics/KPIs | stats-slide |
| Before/after comparison | two-column-slide |
| Hub concept with types | circular-hero-slide |
| Dramatic emphasis (1-3 words) | giant-focus-slide |
| High-energy warning | bold-diagonal-slide |
| Powerful quote | quote-slide |
| List of related items | multi-card-slide |
| Process with steps | floating-cards-slide |
| Technical comparison | two-column-slide |

**Only use content-slide when:**
- None of the above fit
- Information is truly linear
- Need a breather between visual slides

---

## Good Variety Distribution (30-slide presentation)

- Content-slide: 6-7 slides (20-23%)
- Section breaks: 5 slides (17%)
- Visual layouts: 15-16 slides (50-53%)
  - Multi-card: 3-4 slides
  - Two-column: 2-3 slides
  - Stats: 1-2 slides
  - Floating-cards: 2-3 slides
  - Circular-hero: 1-2 slides
  - Giant-focus/Bold-diagonal: 2-3 slides
  - Quote: 1 slide
- Title/Closing: 2-3 slides (7-10%)
