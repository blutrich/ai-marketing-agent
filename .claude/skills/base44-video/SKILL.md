---
name: base44-video
description: Generate Remotion videos from Base44 social posts
metadata:
  tags: base44, video, remotion, linkedin, x, social
---

# Base44 Video Generator

Transform Base44 social posts into Remotion video compositions.

## Brand Colors (MANDATORY)

```typescript
const BASE44_COLORS = {
  bgTop: "#E8F4F8",
  bgBottom: "#FDF5F0",
  bgCard: "#FFFFFF",
  text: "#000000",
  textSecondary: "#666666",
  orange: "#FF983B",
  orangeLight: "#FFE9DF",
  orangeDark: "#EA6020",
};
```

## Animation Rules (MANDATORY)

1. ALL animations MUST use `useCurrentFrame()` - NO CSS animations
2. Use `spring()` for natural motion: `{ damping: 200 }` for smooth
3. Always clamp: `extrapolateRight: 'clamp'`
4. Durations in seconds × fps: `2 * fps` for 2 seconds

## Voice Guidelines

- "builders" not "users"
- "ship" / "go live" not "deploy"
- Action verbs: ship, drop, build
- Lead with outcomes

## Logo (ALWAYS include in first and last scene)

```typescript
<Img src={staticFile("base44_logo.jpeg")} style={{ width: 80, height: 80, borderRadius: 40 }} />
```

## Centering (MANDATORY)

Every AbsoluteFill: `justifyContent: "center", alignItems: "center", textAlign: "center"`
