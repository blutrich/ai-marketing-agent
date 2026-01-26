# Base44 — Brand System

> Visual identity for the AI-first vibe coding platform. Bold orange, dark backgrounds, builder energy.

---

## Brand Philosophy

### Core Principles

1. **Orange is the Hero**
   Base44 Orange (#FF6B00) is our signature. It's energetic, bold, and impossible to miss. Use it for brand moments that need to pop—but don't overuse it or the impact fades.

2. **Dark Mode by Default**
   Our dark theme communicates technical credibility and modern aesthetics. Clean black backgrounds make the orange sing and let content breathe.

3. **Function Over Decoration**
   Every visual element has a job. No gratuitous gradients, no ornamental shapes. If it doesn't help the builder understand or act, it doesn't belong.

4. **Speed in Design**
   Our visuals should feel fast—clean lines, minimal clutter, immediate clarity. The same way our platform turns ideas into apps, our design turns concepts into comprehension.

---

## Logo

### The Base44 Mark

Orange circle with 3 horizontal white lines running through it (resembling a stylized sunrise or stack), paired with "Base44" wordmark in clean dark sans-serif.

**Origin story:** "It's all orange in here, and the $5 logo I bought 9 months ago is now etched everywhere on the walls." — Maor Shlomo

**Logo file**: `.claude/skills/pptx-generator/brands/base44/assets/logo.png`

**Usage rules:**
- Maintain aspect ratio
- Minimum clear space: 20% of logo width on all sides
- Use white version on dark/orange backgrounds
- Use orange/dark version on light backgrounds
- Never stretch, rotate, or add effects to the logo
- The 3 lines in the icon must remain evenly spaced

---

## Color System

### Primary Accent — Base44 Orange

The signature brand color. Energetic, bold, and action-oriented.

| Name | Hex | Use |
|------|-----|-----|
| Base44 Orange | `#FF6B00` | Primary buttons, links, highlights, brand moments |
| Orange Dark | `#E65C00` | Hover states, outlines, emphasis |
| Orange Light | `#FF8533` | Secondary accents, gradient endpoints |
| Orange Pale | `#FFB380` | Tertiary accents, backgrounds |

**Rule:** Base44 Orange is the hero. Use for primary actions and brand emphasis. Don't dilute by overusing—when everything is orange, nothing is.

### Theme Base

**Dark Theme (Default)**
```
Background:     #0a0a0a
Background Alt: #1a1a1a
Surface:        #1f1f1f
Text Primary:   #ffffff
Text Secondary: #b0b0b0
```

### Gradient Usage

Base44 uses signature orange gradients for marketing:
- **Direction:** Top to bottom
- **Top color:** Light cream/beige (#F5F0EB)
- **Bottom color:** Base44 Orange (#FF6B00)
- **Usage:** Hero sections, marketing graphics, social cards

**Dark card gradient:**
- Top: Dark gray (#2a2a2a)
- Bottom: Near-black (#0a0a0a)
- Subtle orange accent line at bottom

---

## Typography

### Font Stack

- **Heading:** Inter — Clean, modern, highly readable at all sizes
- **Body:** Inter — Consistent with headings, excellent for UI and documentation
- **Code:** JetBrains Mono — Developer-focused, ligature support, technical credibility

### Typography Rules

| Element | Font | Weight | Size |
|---------|------|--------|------|
| Display/Hero | Inter | 700 | 36px+ |
| H1 | Inter | 700 | 30px |
| H2 | Inter | 600 | 24px |
| Body | Inter | 400 | 16-18px |
| Code | JetBrains Mono | 400 | 14px |

### Text Color Usage

| Context | Color | Notes |
|---------|-------|-------|
| Headings | #ffffff | Full contrast on dark backgrounds |
| Body | #b0b0b0 | Comfortable reading, reduced eye strain |
| Links/CTAs | #FF6B00 | Base44 Orange with hover effect |
| Code | #ffffff | On dark code background (#141414) |

---

## Spacing System

**Base unit:** 4px

| Token | Value | Use |
|-------|-------|-----|
| `xs` | 4px | Tight spacing, icon gaps |
| `sm` | 8px | Related elements |
| `base` | 16px | Standard padding |
| `lg` | 24px | Section padding |
| `xl` | 32px | Card padding |
| `2xl` | 48px | Section margins |

**Rule:** When in doubt, use multiples of 8px.

---

## Buttons

### Button Types

| Type | Background | Text | Use |
|------|------------|------|-----|
| Primary | #FF6B00 | White | Main actions, CTAs |
| Secondary | #1f1f1f | #ffffff | Secondary actions |
| Ghost | Transparent | #ffffff | Tertiary actions, inline |

### Button Specs

- **Font:** Inter, 500 weight
- **Border radius:** 8px (rounded, approachable)
- **Padding:** 8px 16px (standard), 12px 24px (large)

---

## Signature Elements

These patterns define the Base44 visual identity:

### 1. The Orange Gradient Hero
Full cream-to-orange gradient backgrounds for marketing moments. Bold, warm, energetic. The white logo pops against it.

### 2. Dark Feature Cards
Dark gradient backgrounds (gray to black) with white text. Orange accent line at bottom. Used for documentation and feature announcements.

### 3. Partnership Pills
Pill-shaped white containers on light backgrounds, with orange sync/connection icon between brand logos. Clean, partnership-focused.

### 4. Embossed Headlines
On full orange backgrounds, use slightly darker orange text for an embossed/letterpress effect. Minimal, confident, bold.

---

## Diagrams

### Color Palette for Diagrams

| Semantic Purpose | Fill | Stroke |
|------------------|------|--------|
| Primary/Neutral | `#FF6B00` | `#E65C00` |
| Secondary | `#FF8533` | `#E65C00` |
| Start/Trigger | `#FED7AA` | `#C2410C` |
| End/Success | `#A7F3D0` | `#047857` |
| Warning/Decision | `#FEF3C7` | `#B45309` |
| Error/Stop | `#FECACA` | `#B91C1C` |

### Diagram Rules

- **Background:** White (#FFFFFF) for maximum readability
- **Text color:** Dark (#1a1a1a) for contrast
- **Stroke width:** 2px
- **Rule:** Always pair darker stroke with lighter fill

---

## Quick Reference

### When to Use Base44 Orange

| Use Orange | Don't Use Orange |
|------------|------------------|
| Primary CTAs | Every button |
| Brand moments | Body text |
| Accent highlights | Entire backgrounds (except marketing heroes) |
| Links | Icons that aren't primary actions |
| Marketing heroes | UI chrome |

### Font Usage

| Inter (Heading/Body) | JetBrains Mono (Code) |
|----------------------|------------------------|
| Headlines | Code blocks |
| Body copy | Terminal output |
| Buttons | Technical specs |
| Navigation | File paths |
| UI labels | Inline code |

---

*Last updated: 2026-01-23*
