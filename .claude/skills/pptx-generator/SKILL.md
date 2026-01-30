---
name: pptx-generator
description: |
  Generate and edit presentation slides as PPTX files. Also create LinkedIn carousels and manage reusable slide layouts.

  TRIGGERS - Use this skill when user says:
  - "create slides for [brand]" / "generate presentation for [brand]"
  - "create a carousel for [brand]" / "linkedin carousel"
  - "edit this pptx" / "update the slides"
  - "create a new layout" / "add a layout to the cookbook"
  - Any request mentioning slides, presentations, carousels, PPTX, or layouts

  Creates .pptx files compatible with PowerPoint, Google Slides, and Keynote.
  Creates PDF carousels for LinkedIn (square 1:1 format).
---

# PPTX Slide Generator

Generate professional, on-brand presentation slides using python-pptx.

**Capabilities:**
- **Slide Generation** - Create presentations for any brand in `brands/`
- **Carousel Generation** - Create LinkedIn carousels (square format, PDF)
- **Slide Editing** - Modify existing PPTX files
- **Layout Management** - Create, edit, update cookbook layouts

**Skill resources:** `.claude/skills/pptx-generator/`

---

## ⚠️ CRITICAL: Batch Generation Rules

**NEVER generate more than 5 slides at once.**

| Rule | Details |
|------|---------|
| Max slides per batch | **5** |
| After each batch | **STOP and validate** |
| After ALL batches | **COMBINE into single file and DELETE part files** |

---

## ⚠️ PREREQUISITE: Brand Check

**Before generating, check if brands exist:**

```
Glob: .claude/skills/pptx-generator/brands/*/brand.json
```

**If NO brands found:**
1. STOP - Do not proceed
2. Ask: "No brands configured. Would you like me to help create one?"
3. If yes, follow Creating a New Brand below
4. If no, offer generic styling as fallback

---

## Creating a New Brand

### Step 1: Read the template
```
Read: .claude/skills/pptx-generator/brands/template/README.md
Read: .claude/skills/pptx-generator/brands/template/brand.json
Read: .claude/skills/pptx-generator/brands/template/config.json
```

### Step 2: Gather brand information

| Required | Description |
|----------|-------------|
| Brand name | Folder name (lowercase, no spaces) |
| Colors | Background, text, accent (hex codes) |
| Fonts | Heading, body, code font |

### Step 3: Create brand files

```bash
mkdir -p .claude/skills/pptx-generator/brands/{brand-name}
```

**brand.json:**
```json
{
  "name": "Brand Name",
  "colors": {
    "background": "hex-without-hash",
    "text": "hex-without-hash",
    "accent": "hex-without-hash"
  },
  "fonts": {
    "heading": "Font Name",
    "body": "Font Name"
  }
}
```

**config.json:**
```json
{
  "output": {
    "directory": "output/{brand}",
    "naming": "{name}-{date}"
  },
  "generation": {
    "slides_per_batch": 5,
    "auto_combine": true
  }
}
```

---

## Skill Modes

### Mode 1: Generate Presentation Slides
→ See detailed guide in [GENERATION.md](GENERATION.md)
→ Layout selection in [LAYOUTS.md](LAYOUTS.md)

### Mode 2: Generate LinkedIn Carousels
→ See [CAROUSELS.md](CAROUSELS.md)

### Mode 3: Manage Cookbook Layouts
→ See [LAYOUT-CRUD.md](LAYOUT-CRUD.md)

---

## Mode 1: Quick Reference

### Step 1: Brand Discovery

```
Read: .claude/skills/pptx-generator/brands/{brand}/brand.json
Read: .claude/skills/pptx-generator/brands/{brand}/config.json
Glob: .claude/skills/pptx-generator/brands/{brand}/*.md
```

### Step 2: Layout Discovery

**⚠️ Read ALL layout frontmatters before selecting:**

```
Glob: .claude/skills/pptx-generator/cookbook/*.py
```

Read first 40 lines of each to extract `# /// layout` block.

**See [LAYOUTS.md](LAYOUTS.md) for detailed selection guide.**

### Step 3: Slide Planning

**Create a plan table BEFORE generating:**

```markdown
| # | Layout | Title | Key Content |
|---|--------|-------|-------------|
| 1 | title-slide | [Title] | [Subtitle] |
| 2 | multi-card-slide | [Title] | [3-5 cards] |
```

**Variety checks:**
- [ ] Content-slide <25% of total
- [ ] No 3+ consecutive same-layout
- [ ] Visual layouts 50%+ of slides

### Step 4: Generate (Max 5 slides per batch)

**⚠️ CRITICAL: Set background on every slide:**

```python
slide = prs.slides.add_slide(prs.slide_layouts[6])
slide.background.fill.solid()
slide.background.fill.fore_color.rgb = hex_to_rgb(BRAND_BG)
```

**Execute via heredoc:**
```bash
uv run --with python-pptx==1.0.2 python << 'EOF'
# Code here
EOF
```

### Step 5: Validate

Check after each batch:
- No white backgrounds
- No duplicate titles
- Proper spacing
- Colors match brand

### Step 6: Combine & Output

After all batches validated, combine into single file.

**See [GENERATION.md](GENERATION.md) for combining code.**

---

## Technical Quick Reference

**Dimensions:** 13.333" × 7.5" (16:9)

**Always use:** `prs.slide_layouts[6]` (blank)

**See [TECHNICAL.md](TECHNICAL.md) for full reference.**

---

## Checklist

**For Slide Generation:**
- [ ] Read brand.json, config.json
- [ ] Read ALL cookbook layout frontmatters
- [ ] Create slide plan table
- [ ] **VARIETY CHECK passed**
- [ ] Generate MAX 5 slides per batch
- [ ] Validate each batch
- [ ] Combine into final file
- [ ] Delete part files

**For Creating Layouts:**
- [ ] Study existing layouts
- [ ] Design with decorative elements
- [ ] Write detailed frontmatter
- [ ] Test the layout

---

## Reference Files

| File | Content |
|------|---------|
| [LAYOUTS.md](LAYOUTS.md) | Layout selection, visual variety |
| [GENERATION.md](GENERATION.md) | Batch generation, combining |
| [CAROUSELS.md](CAROUSELS.md) | LinkedIn carousel creation |
| [LAYOUT-CRUD.md](LAYOUT-CRUD.md) | Creating/editing layouts |
| [TECHNICAL.md](TECHNICAL.md) | python-pptx code reference |

---

## Brand Data Loading (Base44)

**For Base44 presentations:**
- `Read: brands/base44/brand.json` - Colors, fonts
- `Read: brands/base44/tone-of-voice.md` - Voice guidelines
- `Read: brands/base44/facts/metrics.md` - Stats
- `Read: brands/base44/case-studies/index.md` - Stories
