# LinkedIn Carousel Generation

Create multi-page PDFs in square (1:1) format for LinkedIn.

## Carousel vs Presentation

| Aspect | Presentation | Carousel |
|--------|--------------|----------|
| Dimensions | 16:9 (13.333" × 7.5") | 1:1 (7.5" × 7.5") |
| Layouts | `cookbook/*.py` | `cookbook/carousels/*.py` |
| Output | PPTX | PDF (via PPTX conversion) |
| Slides | 10-50+ typical | 5-10 optimal |
| Text size | Standard | Larger (mobile readable) |
| Content | Detailed | One idea per slide |

---

## Carousel Layout Discovery

```
Glob: .claude/skills/pptx-generator/cookbook/carousels/*.py
```

**Available carousel layouts:**

| Layout | Purpose | Best For |
|--------|---------|----------|
| `hook-slide` | Opening attention-grabber | First slide only |
| `single-point-slide` | One key point | Body content |
| `numbered-point-slide` | Numbered list item | Listicles, steps |
| `quote-slide` | Quote with attribution | Social proof |
| `cta-slide` | Call to action | Last slide only |

---

## Carousel Planning

**Typical structure (5-10 slides):**

```markdown
| # | Layout | Content |
|---|--------|---------|
| 1 | hook-slide | Attention-grabbing hook |
| 2-8 | single-point or numbered-point | Body content |
| 9/10 | cta-slide | Call to action |
```

**Content rules:**
- **One idea per slide** - Don't cram
- **Large text** - Readable on mobile
- **Short copy** - Max 50 chars headlines, 150 body
- **Clear flow** - Each slide stands alone
- **Strong hook** - First slide stops scroll
- **Clear CTA** - Last slide tells what to do

---

## Generate Carousel

**Square dimensions (1:1):**
```python
prs.slide_width = Inches(7.5)
prs.slide_height = Inches(7.5)
```

**Execution:**
```bash
uv run --with python-pptx==1.0.2 python << 'SCRIPT'
from pptx import Presentation
from pptx.util import Inches

prs = Presentation()
prs.slide_width = Inches(7.5)
prs.slide_height = Inches(7.5)

# Generate slides...

prs.save("output/{brand}/carousel.pptx")
SCRIPT
```

---

## Export to PDF

LinkedIn requires PDF for carousel posts.

**Option A: LibreOffice (recommended)**
```bash
libreoffice --headless --convert-to pdf --outdir output/{brand} output/{brand}/carousel.pptx
```

**Option B: soffice**
```bash
soffice --headless --convert-to pdf output/{brand}/carousel.pptx
```

**Note:** On macOS: `brew install --cask libreoffice`

---

## Output Files

Save both:
- `output/{brand}/{name}-carousel.pptx` - Editable source
- `output/{brand}/{name}-carousel.pdf` - LinkedIn-ready

---

## Carousel Checklist

- [ ] Read brand configuration
- [ ] Read carousel layout frontmatters
- [ ] Plan structure (hook → body → CTA)
- [ ] Keep text SHORT
- [ ] Use 7.5" × 7.5" dimensions
- [ ] Generate PPTX
- [ ] Validate output
- [ ] Export to PDF
- [ ] Test in LinkedIn preview
