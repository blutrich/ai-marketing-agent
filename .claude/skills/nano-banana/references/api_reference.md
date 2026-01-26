# Gemini Imagen 3 API Reference

## Model

- **Model ID**: `imagen-3.0-generate-002`
- **Provider**: Google AI (Gemini)
- **Capability**: Text-to-image generation

## Authentication

Get an API key from Google AI Studio: https://aistudio.google.com/apikey

```bash
export GOOGLE_API_KEY="your-api-key"
```

## Python SDK

### Installation

```bash
pip install google-genai Pillow
```

### Basic Usage

```python
from google import genai
from google.genai import types

client = genai.Client(api_key="your-api-key")

response = client.models.generate_images(
    model="imagen-3.0-generate-002",
    prompt="A serene mountain landscape at sunset",
    config=types.GenerateImagesConfig(
        number_of_images=1,
        aspect_ratio="16:9",
    ),
)

# Access generated image
image_bytes = response.generated_images[0].image.image_bytes
```

## Configuration Options

### GenerateImagesConfig

| Parameter | Type | Description |
|-----------|------|-------------|
| `number_of_images` | int | Number of images to generate (1-4) |
| `aspect_ratio` | str | Image dimensions ratio |
| `safety_filter_level` | str | Content filtering level |
| `person_generation` | str | People in images setting |

### Aspect Ratios

| Ratio | Resolution | Use Case |
|-------|------------|----------|
| `1:1` | 1024x1024 | Social squares, LinkedIn carousels |
| `3:4` | 768x1024 | Instagram, mobile stories |
| `4:3` | 1024x768 | Blog headers, presentations |
| `16:9` | 1536x640 | YouTube thumbnails, wide banners |
| `9:16` | 640x1536 | Vertical stories, mobile ads |

### Safety Filter Levels

| Level | Description |
|-------|-------------|
| `BLOCK_LOW_AND_ABOVE` | Strictest filtering |
| `BLOCK_MEDIUM_AND_ABOVE` | Default filtering |
| `BLOCK_ONLY_HIGH` | Permissive filtering |

## Response Format

```python
response.generated_images[0].image.image_bytes  # PNG bytes
```

## Error Handling

```python
if not response.generated_images:
    # Prompt may have been blocked by safety filters
    print("No images generated")
```

## Pricing

- Standard quality: ~$0.04 per image
- High quality: ~$0.134 per image

## Rate Limits

- 10 requests per minute (free tier)
- Higher limits available with paid plans

## Prompt Best Practices

1. **Be specific**: Include details about subject, style, lighting, colors
2. **Describe composition**: Mention camera angle, framing, background
3. **Add style keywords**: "professional photography", "minimal design", "3D render"
4. **Include colors**: Reference specific hex codes for brand consistency
5. **Avoid negatives**: Describe what you want, not what you don't want
