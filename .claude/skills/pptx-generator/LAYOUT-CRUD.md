# Layout CRUD Operations

Create, edit, update, and delete cookbook layouts.

## Creating New Layouts

### Step 1: Study existing layouts
```
Glob: .claude/skills/pptx-generator/cookbook/*.py
```

Read 2-3 layouts to understand:
- Code structure and imports
- Brand variable usage
- Decorative element patterns
- Positioning conventions

### Step 2: Design with quality standards

**MUST be production-ready:**
- Professional, polished appearance
- Visually engaging (not plain)
- Distinctive decorative elements
- Strong visual hierarchy
- Proper whitespace

**Use appropriate elements:**
- **Charts** - Pie, doughnut, bar for data
- **Images** - Placeholder shapes
- **Shapes** - Circles, rectangles for visual interest
- **Cards** - Floating cards with shadows
- **Geometric patterns** - Bold shapes at corners/edges

**Avoid:**
- Plain text-only layouts
- Generic bullet points
- Tiny decorative elements
- Centered-everything compositions

### Step 3: Write the layout file

```python
#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = ["python-pptx==1.0.2"]
# ///
# /// layout
# name = "layout-name"
# purpose = "When to use this layout"
# best_for = [
#     "Ideal use case 1",
#     "Ideal use case 2",
# ]
# avoid_when = [
#     "Situation to avoid - and what to use instead",
# ]
# max_items = 5
# instructions = [
#     "Specific tip 1",
#     "Specific tip 2",
# ]
# ///
"""
LAYOUT: [Name]
PURPOSE: [When to use]

CUSTOMIZE:
- [List customizable elements]
"""

# ... implementation
```

**Required frontmatter fields:**

| Field | Description |
|-------|-------------|
| `name` | Layout identifier |
| `purpose` | Clear one-line description |
| `best_for` | Detailed array of ideal scenarios |
| `avoid_when` | Specific situations with alternatives |
| `instructions` | Actionable usage tips |

**Optional fields:**
| Field | Description |
|-------|-------------|
| `max_*` / `min_*` | Hard limits on items |
| `*_max_chars` | Character limits |

### Writing good frontmatter

✅ **DO: Be specific and actionable**
```python
# avoid_when = [
#     "More than 3 items - use multi-card-slide instead",
#     "Long card titles (over 15 chars) - abbreviate or use content-slide",
# ]
```

❌ **DON'T: Be vague**
```python
# avoid_when = ["Too many items", "Wrong content"]
```

### Step 4: Save to cookbook
```
.claude/skills/pptx-generator/cookbook/{layout-name}-slide.py
```

### Step 5: Test by generating a sample

---

## Editing Existing Layouts

1. **Find the layout:**
   ```
   Glob: .claude/skills/pptx-generator/cookbook/*{name}*.py
   ```

2. **Read and understand** current structure

3. **Make modifications** preserving:
   - Script header format
   - Brand variable naming
   - Docstring format

4. **Update frontmatter** if changes affect:
   - `best_for` scenarios
   - `avoid_when` situations
   - Item limits
   - Usage instructions

5. **Save back** to the same file

6. **Test** the modified layout

---

## Updating/Improving Layouts

### Analyze current weaknesses:
- Is it visually engaging?
- Does it have enough decorative elements?
- Is there good visual hierarchy?
- Does it use space well?

### Apply improvements:
- Add bold geometric shapes
- Improve color usage
- Add depth (shadows, overlapping)
- Better typography sizing
- More distinctive decorative elements

### Preserve functionality
Don't break what works.

### Review frontmatter
- Are `best_for` and `avoid_when` still accurate?
- Do `instructions` reflect new constraints?
- Update limits if element counts changed

---

## Deleting Layouts

```bash
rm .claude/skills/pptx-generator/cookbook/{layout-name}.py
```
