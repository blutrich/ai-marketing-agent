#!/usr/bin/env python3
"""
Add Base44-style text overlay to images.
Creates chat-input style overlays like "This year I will... [prompt]"
High-quality rendering with anti-aliasing.
"""

import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Base44 colors
ACCENT = (255, 152, 59)  # #FF983B
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Render at 2x scale for sharper text, then downscale
RENDER_SCALE = 2

# Default output directory (current working directory)
DEFAULT_OUTPUT_DIR = Path.cwd()

# Font paths
FONTS = [
    Path.home() / "Library/Fonts/STKMiso-Light.ttf",
    Path.home() / "Library/Fonts/STKMiso-Regular.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
]

# Logo path
LOGO_PATH = Path.home() / ".claude/skills/pptx-generator/brands/base44/assets/logo.png"


def get_font(size: int) -> ImageFont.FreeTypeFont:
    """Load the best available font at scaled size for crisp rendering."""
    scaled_size = size * RENDER_SCALE
    for font_path in FONTS:
        if font_path.exists():
            try:
                return ImageFont.truetype(str(font_path), scaled_size)
            except:
                continue
    return ImageFont.load_default()


def add_logo(overlay: Image.Image, position: str = "top-left", size: int = 120) -> Image.Image:
    """Add Base44 logo to overlay at scaled resolution."""
    if not LOGO_PATH.exists():
        print(f"Warning: Logo not found at {LOGO_PATH}")
        return overlay

    logo = Image.open(LOGO_PATH).convert('RGBA')

    # Resize logo (scaled for high-res rendering)
    scaled_size = size * RENDER_SCALE
    aspect = logo.width / logo.height
    logo = logo.resize((scaled_size, int(scaled_size / aspect)), Image.Resampling.LANCZOS)

    w, h = overlay.size
    margin = 40 * RENDER_SCALE

    # Position logo
    if position == "top-left":
        x, y = margin, margin
    elif position == "top-right":
        x, y = w - logo.width - margin, margin
    elif position == "bottom-left":
        x, y = margin, h - logo.height - margin
    elif position == "bottom-right":
        x, y = w - logo.width - margin, h - logo.height - margin
    elif position == "top-center":
        x, y = (w - logo.width) // 2, margin
    else:
        x, y = margin, margin

    overlay.paste(logo, (x, y), logo)
    return overlay


def add_chat_overlay(
    image_path: str,
    headline: str,
    input_text: str,
    output_path: str = None,
    position: str = "bottom",
    logo: str = None,
    logo_size: int = 120,
) -> str:
    """
    Add chat-style text overlay to an image.
    Renders at 2x resolution for crisp text, then downscales.

    Args:
        image_path: Path to source image
        headline: Text above the input box (e.g., "This year I will")
        input_text: Text inside the chat input (e.g., "Build my app from bed")
        output_path: Where to save (default: adds -overlay suffix)
        position: "bottom", "center", or "top"
        logo: Logo position (top-left, top-right, etc.) or None for no logo
        logo_size: Logo width in pixels

    Returns:
        Path to the saved image
    """
    # Load image and upscale for high-quality rendering
    img = Image.open(image_path)
    orig_w, orig_h = img.size

    # Upscale image for rendering
    w = orig_w * RENDER_SCALE
    h = orig_h * RENDER_SCALE
    img = img.resize((w, h), Image.Resampling.LANCZOS)

    # Load fonts (already scaled in get_font)
    font_headline = get_font(56)
    font_input = get_font(36)

    # Create overlay at scaled size
    overlay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Add logo if requested
    if logo:
        overlay = add_logo(overlay, logo, logo_size)
        draw = ImageDraw.Draw(overlay)

    # Calculate positions (scaled)
    if position == "bottom":
        headline_y = h - (200 * RENDER_SCALE)
        box_y = h - (120 * RENDER_SCALE)
    elif position == "center":
        headline_y = h // 2 - (40 * RENDER_SCALE)
        box_y = h // 2 + (20 * RENDER_SCALE)
    else:  # top
        headline_y = 100 * RENDER_SCALE
        box_y = 160 * RENDER_SCALE

    # Draw headline with shadow
    headline_x = w // 2
    shadow_offset = 3 * RENDER_SCALE
    draw.text((headline_x + shadow_offset, headline_y + shadow_offset), headline,
              font=font_headline, fill=(0, 0, 0, 150), anchor="mm")
    draw.text((headline_x, headline_y), headline, font=font_headline,
              fill=(255, 255, 255, 255), anchor="mm")

    # Chat input box (scaled)
    box_width = min(520 * RENDER_SCALE, w - 80 * RENDER_SCALE)
    box_height = 64 * RENDER_SCALE
    box_x = (w - box_width) // 2

    # White rounded rectangle
    draw.rounded_rectangle(
        [box_x, box_y, box_x + box_width, box_y + box_height],
        radius=32 * RENDER_SCALE,
        fill=(255, 255, 255, 250)
    )

    # Input text
    draw.text((box_x + 28 * RENDER_SCALE, box_y + box_height // 2), input_text,
              font=font_input, fill=(0, 0, 0, 255), anchor="lm")

    # Orange send button
    btn_size = 48 * RENDER_SCALE
    btn_x = box_x + box_width - btn_size - 8 * RENDER_SCALE
    btn_y = box_y + (box_height - btn_size) // 2
    draw.ellipse([btn_x, btn_y, btn_x + btn_size, btn_y + btn_size],
                 fill=ACCENT + (255,))

    # Arrow in button
    cx = btn_x + btn_size // 2
    cy = btn_y + btn_size // 2
    arrow_scale = 12 * RENDER_SCALE
    arrow_width = 10 * RENDER_SCALE
    draw.polygon([
        (cx, cy - arrow_scale),
        (cx + arrow_width, cy + arrow_scale // 2),
        (cx - arrow_width, cy + arrow_scale // 2)
    ], fill=(255, 255, 255, 255))

    # Composite at high resolution
    img = img.convert('RGBA')
    result = Image.alpha_composite(img, overlay)

    # Downscale with high-quality resampling for anti-aliased result
    result = result.resize((orig_w, orig_h), Image.Resampling.LANCZOS)
    result = result.convert('RGB')

    # Save at high quality to default output directory
    if not output_path:
        p = Path(image_path)
        DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        output_path = str(DEFAULT_OUTPUT_DIR / f"{p.stem}-overlay.png")

    result.save(output_path, quality=95)
    print(f"Saved: {output_path}")
    return output_path


def add_simple_text(
    image_path: str,
    text: str,
    output_path: str = None,
    position: str = "center",
    color: str = "white",
    size: int = 64,
    logo: str = None,
    logo_size: int = 120,
) -> str:
    """
    Add simple text overlay to an image.

    Args:
        image_path: Path to source image
        text: Text to add
        output_path: Where to save
        position: "top", "center", "bottom"
        color: "white", "black", or "accent"
        size: Font size
        logo: Logo position or None
        logo_size: Logo width in pixels
    """
    img = Image.open(image_path)
    w, h = img.size

    font = get_font(size)

    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))

    # Add logo if requested
    if logo:
        overlay = add_logo(overlay, logo, logo_size)

    draw = ImageDraw.Draw(overlay)

    # Position
    x = w // 2
    if position == "top":
        y = 100
    elif position == "bottom":
        y = h - 100
    else:
        y = h // 2

    # Color
    colors = {
        "white": (255, 255, 255, 255),
        "black": (0, 0, 0, 255),
        "accent": ACCENT + (255,),
    }
    fill = colors.get(color, (255, 255, 255, 255))

    # Shadow + text
    draw.text((x + 2, y + 2), text, font=font, fill=(0, 0, 0, 150), anchor="mm")
    draw.text((x, y), text, font=font, fill=fill, anchor="mm")

    # Composite
    img = img.convert('RGBA')
    result = Image.alpha_composite(img, overlay)
    result = result.convert('RGB')

    if not output_path:
        p = Path(image_path)
        output_path = str(p.parent / f"{p.stem}-text{p.suffix}")

    result.save(output_path)
    print(f"Saved: {output_path}")
    return output_path


def add_logo_only(
    image_path: str,
    position: str = "top-left",
    logo_size: int = 120,
    output_path: str = None,
) -> str:
    """
    Add only the Base44 logo to an image (no text).
    """
    img = Image.open(image_path)
    orig_w, orig_h = img.size

    # Upscale for quality
    w = orig_w * RENDER_SCALE
    h = orig_h * RENDER_SCALE
    img = img.resize((w, h), Image.Resampling.LANCZOS)

    # Create overlay
    overlay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    overlay = add_logo(overlay, position, logo_size)

    # Composite
    img = img.convert('RGBA')
    result = Image.alpha_composite(img, overlay)

    # Downscale
    result = result.resize((orig_w, orig_h), Image.Resampling.LANCZOS)
    result = result.convert('RGB')

    # Save
    if not output_path:
        p = Path(image_path)
        DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        output_path = str(DEFAULT_OUTPUT_DIR / f"{p.stem}-logo.png")

    result.save(output_path, quality=95)
    print(f"Saved: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Add overlays to images")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Logo only command
    logo_parser = subparsers.add_parser("logo", help="Add Base44 logo only (no text)")
    logo_parser.add_argument("image", help="Source image path")
    logo_parser.add_argument("--position", choices=["top-left", "top-right", "top-center", "bottom-left", "bottom-right"],
                            default="top-left", help="Logo position")
    logo_parser.add_argument("--size", type=int, default=120, help="Logo width in pixels")
    logo_parser.add_argument("-o", "--output", help="Output path")

    # Chat overlay command
    chat_parser = subparsers.add_parser("chat", help="Add chat-style overlay (headline + input box)")
    chat_parser.add_argument("image", help="Source image path")
    chat_parser.add_argument("--headline", default="This year I will", help="Headline text")
    chat_parser.add_argument("--input", required=True, help="Chat input text")
    chat_parser.add_argument("-o", "--output", help="Output path")
    chat_parser.add_argument("--position", choices=["top", "center", "bottom"], default="bottom")
    chat_parser.add_argument("--logo", choices=["top-left", "top-right", "top-center", "bottom-left", "bottom-right"],
                            help="Add Base44 logo at position")
    chat_parser.add_argument("--logo-size", type=int, default=120, help="Logo width in pixels")

    # Simple text command
    text_parser = subparsers.add_parser("text", help="Add simple text overlay")
    text_parser.add_argument("image", help="Source image path")
    text_parser.add_argument("--text", required=True, help="Text to add")
    text_parser.add_argument("-o", "--output", help="Output path")
    text_parser.add_argument("--position", choices=["top", "center", "bottom"], default="center")
    text_parser.add_argument("--color", choices=["white", "black", "accent"], default="white")
    text_parser.add_argument("--size", type=int, default=64, help="Font size")
    text_parser.add_argument("--logo", choices=["top-left", "top-right", "top-center", "bottom-left", "bottom-right"],
                            help="Add Base44 logo at position")
    text_parser.add_argument("--logo-size", type=int, default=120, help="Logo width in pixels")

    args = parser.parse_args()

    if args.command == "logo":
        add_logo_only(args.image, args.position, args.size, args.output)
    elif args.command == "chat":
        add_chat_overlay(args.image, args.headline, args.input, args.output, args.position,
                        args.logo, args.logo_size)
    elif args.command == "text":
        add_simple_text(args.image, args.text, args.output, args.position, args.color, args.size,
                       args.logo, args.logo_size)


if __name__ == "__main__":
    main()
