#!/usr/bin/env python3
"""
Generate images using Google's Imagen 3 (Gemini) API.
Requires: pip install google-genai Pillow
"""

import argparse
import json
import os
import sys
from pathlib import Path

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Error: google-genai not installed. Run: pip install google-genai")
    sys.exit(1)

try:
    from PIL import Image
    import io
except ImportError:
    print("Error: Pillow not installed. Run: pip install Pillow")
    sys.exit(1)


# Size presets (aspect ratios)
SIZE_PRESETS = {
    "square": "1:1",      # 1024x1024 - LinkedIn carousels, Instagram
    "portrait": "3:4",    # 768x1024 - Stories, mobile
    "landscape": "4:3",   # 1024x768 - Blog headers, Twitter
    "wide": "16:9",       # 1536x640 - YouTube thumbnails
}

# Style modifiers - always include high resolution
STYLE_MODIFIERS = {
    "photo": "professional photography, ultra high resolution, 4K, extremely detailed, sharp focus, realistic",
    "illustration": "digital illustration, ultra high resolution, 4K, clean vector style, modern design, sharp details",
    "minimal": "minimalist design, ultra high resolution, 4K, clean lines, simple shapes, modern aesthetic, crisp",
    "3d": "3D render, ultra high resolution, 4K, soft lighting, glossy materials, professional, detailed",
}

# Brand directory path
BRANDS_DIR = Path.home() / ".claude/skills/pptx-generator/brands"

# Default output directory (current working directory)
DEFAULT_OUTPUT_DIR = Path.cwd()


def load_brand(brand_name: str) -> dict:
    """Load brand configuration from pptx-generator brands directory."""
    brand_path = BRANDS_DIR / brand_name / "brand.json"
    if not brand_path.exists():
        available = [d.name for d in BRANDS_DIR.iterdir() if d.is_dir()]
        raise ValueError(
            f"Brand '{brand_name}' not found. Available: {', '.join(available)}"
        )

    with open(brand_path) as f:
        return json.load(f)


def build_brand_style(brand: dict) -> str:
    """Convert brand config to style prompt suffix."""
    colors = brand.get("colors", {})
    gradients = brand.get("gradients", {})

    parts = []

    # Background colors
    bg = colors.get("background", "")
    bg_alt = colors.get("background_alt", "")
    if bg and bg_alt:
        parts.append(f"light gradient background from #{bg} to #{bg_alt}")
    elif bg:
        parts.append(f"#{bg} background")

    # Accent color
    accent = colors.get("accent", "")
    if accent:
        parts.append(f"#{accent} accent color")

    # Text color
    text = colors.get("text", "")
    if text:
        parts.append(f"#{text} for text elements")

    # Add brand aesthetic
    desc = brand.get("description", "")
    if "light" in desc.lower():
        parts.append("clean and light aesthetic")
    if "modern" in desc.lower() or "minimal" in desc.lower():
        parts.append("modern minimal design")

    return ", ".join(parts) if parts else ""


def generate_image(
    prompt: str,
    output_path: str = "generated_image.png",
    size: str = "square",
    style: str = "photo",
    brand: str = None,
    api_key: str = None,
) -> str:
    """
    Generate an image using Imagen 3 via Gemini API.

    Args:
        prompt: Text description of the image to generate
        output_path: Where to save the generated image
        size: Size preset (square, portrait, landscape, wide)
        style: Style preset (photo, illustration, minimal, 3d)
        brand: Brand name to load colors from (e.g., "base44")
        api_key: Google AI API key (defaults to GOOGLE_API_KEY env var)

    Returns:
        Path to the generated image
    """
    # Get API key
    api_key = api_key or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "API key required. Set GOOGLE_API_KEY environment variable or pass --api-key"
        )

    # Initialize client
    client = genai.Client(api_key=api_key)

    # Build enhanced prompt
    prompt_parts = [prompt]

    # Add style modifier
    style_suffix = STYLE_MODIFIERS.get(style, "")
    if style_suffix:
        prompt_parts.append(style_suffix)

    # Add brand styling
    if brand:
        brand_config = load_brand(brand)
        brand_style = build_brand_style(brand_config)
        if brand_style:
            prompt_parts.append(brand_style)
            print(f"  Brand: {brand}")
            print(f"  Brand style: {brand_style[:60]}...")

    full_prompt = ", ".join(prompt_parts)

    # Get aspect ratio
    aspect_ratio = SIZE_PRESETS.get(size, "1:1")

    print(f"Generating image...")
    print(f"  Prompt: {prompt[:80]}{'...' if len(prompt) > 80 else ''}")
    print(f"  Size: {size} ({aspect_ratio})")
    print(f"  Style: {style}")

    # Generate image using Gemini 3 Pro (Nano Banana Pro)
    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=full_prompt,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE", "TEXT"],
        ),
    )

    # Check for results and extract image from response
    image_data = None
    if hasattr(response, 'candidates') and response.candidates:
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'inline_data') and part.inline_data:
                image_data = part.inline_data.data
                break

    if not image_data:
        raise RuntimeError("No images generated. The prompt may have been blocked.")

    # Save the image
    image = Image.open(io.BytesIO(image_data))

    # Upscale if below target resolution (2048px on longest side)
    target_size = 2048
    w, h = image.size
    max_dim = max(w, h)
    if max_dim < target_size:
        scale = target_size / max_dim
        new_w = int(w * scale)
        new_h = int(h * scale)
        image = image.resize((new_w, new_h), Image.Resampling.LANCZOS)
        print(f"  Upscaled: {w}x{h} -> {new_w}x{new_h}")

    # Ensure output directory exists - use default if just filename
    output_path = Path(output_path)
    if not output_path.is_absolute() and output_path.parent == Path('.'):
        DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        output_path = DEFAULT_OUTPUT_DIR / output_path.name
    else:
        output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save at high quality
    image.save(output_path, quality=95)
    print(f"  Saved: {output_path} ({image.width}x{image.height})")

    return str(output_path)


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using Google's Imagen 3 (Nano Banana)"
    )
    parser.add_argument(
        "prompt",
        help="Text description of the image to generate"
    )
    parser.add_argument(
        "-o", "--output",
        default="generated_image.png",
        help="Output filename (default: generated_image.png)"
    )
    parser.add_argument(
        "--size",
        choices=["square", "portrait", "landscape", "wide"],
        default="square",
        help="Image size preset (default: square)"
    )
    parser.add_argument(
        "--style",
        choices=["photo", "illustration", "minimal", "3d"],
        default="photo",
        help="Style preset (default: photo)"
    )
    parser.add_argument(
        "--brand",
        help="Brand name to load colors from (e.g., 'base44')"
    )
    parser.add_argument(
        "--api-key",
        help="Google AI API key (defaults to GOOGLE_API_KEY env var)"
    )

    args = parser.parse_args()

    try:
        generate_image(
            prompt=args.prompt,
            output_path=args.output,
            size=args.size,
            style=args.style,
            brand=args.brand,
            api_key=args.api_key,
        )
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
