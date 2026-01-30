# Technical Reference

Python-pptx technical details and code patterns.

## Slide Dimensions

**Presentation (16:9):**
- Width: 13.333 inches
- Height: 7.5 inches
- Safe margins: 0.5 inches

**Carousel (1:1):**
- Width: 7.5 inches
- Height: 7.5 inches

---

## Common Imports

```python
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt
```

---

## Always Use

- Blank layout: `prs.slide_layouts[6]`
- python-pptx version: 1.0.2

---

## Color Conversion

```python
def hex_to_rgb(hex_color: str) -> RGBColor:
    """Convert hex color (with or without #) to RGBColor."""
    h = hex_color.lstrip("#")
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
```

---

## Chart Types

| Type | Constant |
|------|----------|
| Pie | `XL_CHART_TYPE.PIE` |
| Doughnut | `XL_CHART_TYPE.DOUGHNUT` |
| Horizontal bars | `XL_CHART_TYPE.BAR_CLUSTERED` |
| Vertical columns | `XL_CHART_TYPE.COLUMN_CLUSTERED` |
| Line | `XL_CHART_TYPE.LINE` |

### Adding charts:
```python
chart_data = CategoryChartData()
chart_data.categories = ["A", "B", "C"]
chart_data.add_series("Values", [10, 20, 30])

slide.shapes.add_chart(
    XL_CHART_TYPE.DOUGHNUT,
    Inches(x), Inches(y),
    Inches(width), Inches(height),
    chart_data
)
```

---

## Adding Images

```python
slide.shapes.add_picture(
    "path/to/image.png",
    Inches(x), Inches(y),
    width=Inches(w)  # Height auto-calculated
)
```

---

## Adding Shapes

```python
shape = slide.shapes.add_shape(
    MSO_SHAPE.RECTANGLE,
    Inches(x), Inches(y),
    Inches(width), Inches(height)
)
shape.fill.solid()
shape.fill.fore_color.rgb = hex_to_rgb("FF0000")
shape.line.fill.background()  # No border
```

---

## Adding Text Boxes

```python
textbox = slide.shapes.add_textbox(
    Inches(x), Inches(y),
    Inches(width), Inches(height)
)
tf = textbox.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "Your text here"
p.font.size = Pt(24)
p.font.name = "Arial"
p.font.color.rgb = hex_to_rgb("FFFFFF")
p.alignment = PP_ALIGN.CENTER
```

---

## Setting Slide Background

**⚠️ CRITICAL - Must be done for every slide:**

```python
slide = prs.slides.add_slide(prs.slide_layouts[6])
slide.background.fill.solid()
slide.background.fill.fore_color.rgb = hex_to_rgb(BRAND_BG)
```

---

## Preview All Layouts

```bash
uv run .claude/skills/pptx-generator/generate-cookbook-preview.py
```

Generates `cookbook-preview.pptx` with every layout.

---

## Editing Existing PPTX

```python
from pptx import Presentation

# Read existing file
prs = Presentation("path/to/existing.pptx")

# Analyze
print(f"Slides: {len(prs.slides)}")

# Modify slides...

# Save to new location (don't overwrite original)
prs.save("output/modified.pptx")
```
