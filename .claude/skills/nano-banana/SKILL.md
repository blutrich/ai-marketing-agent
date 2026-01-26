---
name: nano-banana
description: Generate marketing images using Google's Imagen 3 (Nano Banana) model. Use when the user wants to create product mockups, social media visuals, blog hero images, carousel graphics, or any AI-generated marketing imagery. Triggers on requests like "generate an image of...", "create a visual for...", "make a mockup showing...", "design an image", or any image generation request for marketing content.
---

# Nano Banana Image Generator

Generate high-quality marketing images using Google's Gemini API + add text overlays.

## Setup

```bash
export GOOGLE_API_KEY="your-api-key"
pip install google-genai Pillow
```

## Quick Start

```bash
# Generate image with brand colors
python3 scripts/generate_image.py "Person on train using phone" --brand base44 --style photo -o photo.png

# Add chat-style text overlay
python3 scripts/add_text_overlay.py chat photo.png --headline "This year I will" --input "Build my app on the train" -o final.png
```

## Image Generation

```bash
python3 scripts/generate_image.py "prompt" [options]

Options:
  -o, --output    Output filename
  --size          square | portrait | landscape | wide
  --style         photo | illustration | minimal | 3d
  --brand         Brand name (e.g., "base44")
```

### Lifestyle Photo Prompts

```bash
# Train
"Young professional on train using smartphone, morning light, editorial photography"

# Couch
"Person relaxed on couch using phone, cozy living room, warm natural lighting"

# Bed
"Person in bed at night using smartphone, soft phone glow, intimate moment"

# Coffee shop
"Creative professional in coffee shop building app on phone, ambient lighting"
```

## Text Overlays

### Chat-Style Overlay (like Base44 ads)

```bash
python3 scripts/add_text_overlay.py chat IMAGE --headline "TEXT" --input "CHAT TEXT" [options]

Options:
  --headline      Text above input box (default: "This year I will")
  --input         Text inside chat input (required)
  --position      top | center | bottom (default: bottom)
  -o, --output    Output path
```

Example:
```bash
python3 scripts/add_text_overlay.py chat photo.png \
  --headline "This year I will" \
  --input "Build my app from bed" \
  -o ad-final.png
```

### Simple Text Overlay

```bash
python3 scripts/add_text_overlay.py text IMAGE --text "TEXT" [options]

Options:
  --text          Text to add (required)
  --position      top | center | bottom
  --color         white | black | accent
  --size          Font size (default: 64)
  -o, --output    Output path
```

## Full Workflow Example

```bash
# 1. Generate lifestyle photo
python3 scripts/generate_image.py \
  "Person in cozy kitchen cooking, using phone on counter, warm lighting" \
  --brand base44 --style photo -o cooking.png

# 2. Add Base44-style chat overlay
python3 scripts/add_text_overlay.py chat cooking.png \
  --headline "This year I will" \
  --input "Order less takeout" \
  -o cooking-ad.png
```

## Brand Integration

Uses STK Miso Light font and Base44 colors (#FF983B accent) automatically.

## API Reference

See `references/api_reference.md` for Gemini API docs.
