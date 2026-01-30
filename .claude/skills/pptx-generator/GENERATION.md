# Slide Generation Guide

Detailed instructions for planning, generating, and combining slides.

## Slide Planning (ALWAYS DO THIS)

**Before generating ANY slides, create a written plan.**

### Create a slide plan table:

```markdown
| # | Layout | Title | Key Content | Notes |
|---|--------|-------|-------------|-------|
| 1 | title-slide | [Title] | [Subtitle, author] | Opening |
| 2 | content-slide | [Title] | [3-4 bullets] | Main concepts |
| 3 | stats-slide | [Title] | [2-3 metrics] | Impact data |
```

### Planning checklist:
- [ ] No duplicate titles across slides
- [ ] Logical flow from slide to slide
- [ ] Appropriate layout for each content type
- [ ] Content fits the chosen layout
- [ ] Batches are logically grouped (5 slides max)
- [ ] **VARIETY CHECK: Content-slide <25% of total**
- [ ] **VARIETY CHECK: No 3+ consecutive same-layout**
- [ ] **VARIETY CHECK: Visual layouts 50%+ of presentation**

---

## Content Adaptation

### Presentation Text Formatting Rules

| Element | Rule | Example |
|---------|------|---------|
| Titles | No trailing periods | "Why AI Matters" not "Why AI Matters." |
| Subtitles | No trailing punctuation | "The future of coding" |
| Bullet points | No trailing periods | "Faster development" |
| Stats/Numbers | Clean format | "50%" not "50%." |
| CTAs | No trailing punctuation | "Get Started" |

### Brand Value Mapping

Map brand.json values to layout placeholders:

| Placeholder | brand.json Path |
|-------------|-----------------|
| `BRAND_BG` | `colors.background` |
| `BRAND_TEXT` | `colors.text` |
| `BRAND_ACCENT` | `colors.accent` |
| `BRAND_HEADING_FONT` | `fonts.heading` |
| `BRAND_BODY_FONT` | `fonts.body` |

**Note:** All color values are hex WITHOUT the `#` prefix.

---

## Batch Generation (CRITICAL)

**MAXIMUM 5 SLIDES PER BATCH. Hard limit.**

### Workflow:
1. Generate 1-5 slides in a single PPTX
2. **STOP and review** before generating more
3. Only after validation, continue with next batch
4. Repeat until complete

### ⚠️ CRITICAL: Background Bug Fix

**EVERY slide MUST have its background explicitly set:**

```python
slide = prs.slides.add_slide(prs.slide_layouts[6])
slide.background.fill.solid()  # ← REQUIRED
slide.background.fill.fore_color.rgb = hex_to_rgb(BRAND_BG)  # ← REQUIRED
```

Without this, slides will have WHITE backgrounds.

### Execution

**PREFERRED: Use heredoc:**
```bash
uv run --with python-pptx==1.0.2 python << 'EOF'
# [Code here]
EOF
```

**IF heredoc fails: Use temp directory:**
```bash
mkdir -p .claude/skills/pptx-generator/.tmp
# Write script to .tmp/gen.py
uv run --with python-pptx==1.0.2 python .claude/skills/pptx-generator/.tmp/gen.py
rm .claude/skills/pptx-generator/.tmp/gen.py  # Clean up
```

---

## Quality Validation (MANDATORY)

**After EVERY batch, validate before continuing:**

| Issue | What to Look For | Fix |
|-------|------------------|-----|
| White background | Slide has white instead of brand color | Add background.fill.solid() |
| Duplicate titles | Same title appearing twice | Remove duplicate text boxes |
| Spacing problems | Title too close to content | Increase Y position |
| Text overflow | Content beyond bounds | Reduce font size |
| Wrong colors | Colors not matching brand | Verify hex values |

---

## Combining Batches

**🚨 CRITICAL: Set background when combining presentations.**

When combining, `add_slide()` creates slides with **DEFAULT WHITE BACKGROUNDS**.

```python
from pptx import Presentation
from pptx.dml.color import RGBColor
from pathlib import Path

def hex_to_rgb(hex_color: str) -> RGBColor:
    h = hex_color.lstrip("#")
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

BRAND_BG = "07090F"  # From brand.json

output_dir = Path("output/{brand-name}")
part_files = sorted(output_dir.glob("{name}-part*.pptx"))

if len(part_files) > 1:
    combined = Presentation(part_files[0])

    for part_file in part_files[1:]:
        part_prs = Presentation(part_file)
        for slide in part_prs.slides:
            blank_layout = combined.slide_layouts[6]
            new_slide = combined.slides.add_slide(blank_layout)

            # 🚨 CRITICAL: Set background IMMEDIATELY
            new_slide.background.fill.solid()
            new_slide.background.fill.fore_color.rgb = hex_to_rgb(BRAND_BG)

            # Copy shapes
            for shape in slide.shapes:
                el = shape.element
                new_slide.shapes._spTree.insert_element_before(el, 'p:extLst')

    combined.save(output_dir / "{name}-final.pptx")

    # Clean up part files
    for part_file in part_files:
        part_file.unlink()
```

### Testing checklist after combining:
- [ ] Open the combined PPTX
- [ ] Scroll through ALL slides
- [ ] Verify EVERY slide has correct background
