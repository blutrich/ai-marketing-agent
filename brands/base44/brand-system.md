# Base44 — Brand System

> Visual identity for the AI-first vibe coding platform. Light gradients, dark text, warm orange accents, clean and modern.

---

## Brand Philosophy

### Core Principles

1. **Light and Airy**
   Base44 uses light blue-to-cream gradient backgrounds that feel fresh, approachable, and modern. This creates a welcoming space for builders.

2. **Warm Orange as Accent**
   Base44 Orange (#FF983B) is used sparingly for emphasis—badges, highlights, accent bars. It pops against the light background without overwhelming.

3. **True Black for Readability**
   Primary text is true black (#000000) for maximum readability. Secondary text is medium gray (#666666).

4. **White Cards with Subtle Shadows**
   Content lives in clean white cards with soft shadows. This creates depth and hierarchy on the gradient backgrounds.

5. **Black CTAs**
   Primary buttons are black (#000000) with white text—not orange. This creates strong contrast and clear action points.

---

## Logo

### The Base44 Mark

Orange circle with stylized horizontal lines, paired with "Base44" wordmark.

**Logo file**: `assets/logo.png`

**Usage rules:**
- Use on light backgrounds (gradient or white)
- Maintain aspect ratio
- Minimum clear space: 20% of logo width on all sides
- Never stretch, rotate, or add effects

**Carousel Logo Placement:**
- Logo appears ONLY on the CTA (last) slide
- Content slides should NOT have the logo (fixes Mac Quick Look rendering bug)

---

## Color System

### Background Gradient (Primary)

The signature Base44 look: light blue fading to warm cream.

| Position | Color | Hex |
|----------|-------|-----|
| Top | Light Blue | `#E8F4F8` |
| Bottom | Cream/Peach | `#FDF5F0` |

**CSS:** `linear-gradient(180deg, #E8F4F8 0%, #FDF5F0 100%)`

### Text Colors

| Purpose | Color | Hex |
|---------|-------|-----|
| Primary text | True Black | `#000000` |
| Secondary text | Medium gray | `#666666` |
| Muted text | Light gray | `#999999` |

### Accent Colors (Orange Palette)

| Name | Hex | Use |
|------|-----|-----|
| Orange Core | `#FF983B` | Primary accent - badges, accent bars, highlights |
| Orange Light | `#FFE9DF` | Light backgrounds, subtle highlights |
| Orange Medium | `#FFBFA1` | Secondary accents, hover states |
| Orange Dark | `#EA6020` | Hover/active states |
| Orange Darkest | `#C94001` | Deep emphasis, rare use |

**Rule:** Orange is for accent only—never for large backgrounds or primary buttons.

### Card & Surface Colors

| Surface | Color | Hex |
|---------|-------|-----|
| Card background | White | `#FFFFFF` |
| Card alt | Off-white | `#f9f9f9` |
| Background secondary | Light gray | `#F0F0F0` |
| Code background | Light gray | `#f5f5f5` |

### Button Colors

| Type | Background | Text |
|------|------------|------|
| Primary CTA | Black `#000000` | White `#FFFFFF` |
| Secondary | White `#FFFFFF` | Black `#000000` |
| Accent (rare) | Orange `#FF983B` | White `#FFFFFF` |

---

## Typography

### Font Stack

| Type | Primary | Fallback |
|------|---------|----------|
| Heading | BC Novatica Cyr / STK Miso | Arial |
| Body | Inter | Arial |
| Code | Courier New | monospace |

**Note:** Use Arial as fallback when custom fonts aren't available (e.g., in PPTX generation).

### Typography Rules

| Element | Weight | Size | Color |
|---------|--------|------|-------|
| H1/Display | 700 (Bold) | 48-72pt | `#000000` |
| H2 | 600 (SemiBold) | 36-48pt | `#000000` |
| H3 | 600 | 24-32pt | `#000000` |
| Body | 400 (Regular) | 18-24pt | `#000000` |
| Secondary | 400 | 16-20pt | `#666666` |

---

## Slide Design Patterns

### Pattern 1: Gradient Background + White Cards

**Background:** Light blue to cream gradient
**Content:** White cards with subtle shadow
**Text:** Dark on cards
**Accent:** Orange accent bars on cards

### Pattern 2: Gradient Background + Direct Text

**Background:** Light blue to cream gradient
**Text:** Dark text directly on gradient (for titles, big statements)
**Accent:** Orange for emphasis words or underlines

### Pattern 3: White Background + Colored Elements

**Background:** Pure white
**Cards:** Light gray or cream
**Accent:** Orange highlights

---

## Carousel-Specific Rules

### Logo Placement
- Logo appears ONLY on the CTA (last) slide
- This fixes a Mac Quick Look rendering bug where text stops rendering when the same image appears on multiple slides

### Text Formatting (Critical for Quick Look)
Use workshop-style paragraph formatting:

```python
# CORRECT (works in Quick Look):
p = tf.paragraphs[0]
p.text = "Headline text"
p.font.name = "Arial"
p.font.size = Pt(38)
p.font.bold = True

# INCORRECT (fails in Quick Look):
run = p.add_run()
run.text = "Headline text"
run.font.name = "Arial"
```

---

## Do's and Don'ts

### DO
- Use light gradient backgrounds
- Use true black (#000000) text for readability
- Use white cards for content
- Use orange (#FF983B) sparingly for accents
- Use black for primary CTAs
- Keep designs clean and spacious
- Place logo only on CTA slide for carousels

### DON'T
- Use dark/black backgrounds
- Use white text (except on buttons)
- Use orange for buttons or large areas
- Overuse orange—it should pop, not dominate
- Use heavy shadows or gradients on text
- Place logo on every carousel slide

---

## Quick Reference

| Element | Value |
|---------|-------|
| Background Top | `#E8F4F8` |
| Background Bottom | `#FDF5F0` |
| Background Secondary | `#F0F0F0` |
| Primary Text | `#000000` |
| Secondary Text | `#666666` |
| Accent (Orange Core) | `#FF983B` |
| Accent Light | `#FFE9DF` |
| Accent Medium | `#FFBFA1` |
| Accent Dark | `#EA6020` |
| Card Background | `#FFFFFF` |
| Button Background | `#000000` |
| Card Shadow | `0 4px 24px rgba(0,0,0,0.08)` |

---

*Last updated: 2026-01-24*
