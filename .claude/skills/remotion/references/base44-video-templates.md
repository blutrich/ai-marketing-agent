# Base44 Video Templates for Remotion

## Brand Constants

```typescript
// Base44 brand colors
export const BASE44_COLORS = {
  orange: '#FF6B00',
  orangeLight: '#FF8533',
  orangePale: '#FFB380',
  background: '#0a0a0a',
  backgroundAlt: '#1a1a1a',
  surface: '#1f1f1f',
  text: '#ffffff',
  textSecondary: '#b0b0b0',
  cream: '#F5F0EB', // gradient top
};

// Fonts
export const BASE44_FONTS = {
  heading: 'Inter',
  body: 'Inter',
  code: 'JetBrains Mono',
};
```

## Video Types for Social Posts

### 1. Feature Announcement Video (15-30 sec)
Use for: New feature drops (Gmail, Safe Testing, etc.)

**Structure:**
```
[0-3s]   Base44 logo animation (orange pulse)
[3-8s]   Feature title reveal (big, bold, orange accent)
[8-20s]  Screen recording of feature in action
[20-25s] Key benefit text overlay
[25-30s] CTA + logo lockup
```

**Remotion composition:**
```typescript
export const FeatureAnnouncement: React.FC<{
  featureName: string;
  tagline: string;
  screenRecording: string;
  benefit: string;
}> = ({featureName, tagline, screenRecording, benefit}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  return (
    <AbsoluteFill style={{backgroundColor: BASE44_COLORS.background}}>
      {/* Logo intro: 0-3s */}
      <Sequence from={0} durationInFrames={3 * fps}>
        <LogoReveal />
      </Sequence>

      {/* Feature title: 3-8s */}
      <Sequence from={3 * fps} durationInFrames={5 * fps}>
        <FeatureTitle name={featureName} tagline={tagline} />
      </Sequence>

      {/* Screen recording: 8-20s */}
      <Sequence from={8 * fps} durationInFrames={12 * fps}>
        <OffthreadVideo src={screenRecording} />
      </Sequence>

      {/* Benefit + CTA: 20-30s */}
      <Sequence from={20 * fps}>
        <BenefitCTA text={benefit} />
      </Sequence>
    </AbsoluteFill>
  );
};
```

### 2. Success Story Video (30-60 sec)
Use for: Builder highlights (GiftMyBook, Lunair.ai style)

**Structure:**
```
[0-5s]   Hook: Big number or result ($1M ARR, $50K in 30 days)
[5-15s]  Builder intro + app showcase
[15-35s] The journey (problem → Base44 → result)
[35-50s] App demo / screenshots
[50-60s] Quote + CTA
```

### 3. Quick Demo Video (10-20 sec)
Use for: X posts, feature teasers

**Structure:**
```
[0-2s]   Feature name (text only, fast)
[2-15s]  Screen recording with highlight annotations
[15-20s] "Try it now" + logo
```

### 4. Playful Build Video (20-40 sec)
Use for: X posts (Assaf-style game demos)

**Structure:**
```
[0-5s]   "I built [thing] with Base44"
[5-30s]  Gameplay / demo with energy
[30-35s] Tech stack callout (@greensock @PixiJS etc)
[35-40s] "What should I build next?"
```

## Animation Patterns

### Orange Pulse (Logo/Accent)
```typescript
const orangePulse = interpolate(
  frame,
  [0, 15, 30],
  [1, 1.1, 1],
  { extrapolateRight: 'clamp' }
);

const glowOpacity = interpolate(
  frame,
  [0, 15, 30],
  [0.3, 0.6, 0.3]
);
```

### Text Reveal (Headlines)
```typescript
const textReveal = spring({
  frame,
  fps,
  config: { damping: 12, stiffness: 100 }
});

// Slide up + fade in
transform: `translateY(${interpolate(textReveal, [0, 1], [30, 0])}px)`,
opacity: textReveal,
```

### Gradient Background
```typescript
<AbsoluteFill
  style={{
    background: `linear-gradient(180deg, ${BASE44_COLORS.cream} 0%, ${BASE44_COLORS.orange} 100%)`,
  }}
/>
```

### Dark Card Overlay
```typescript
<div style={{
  background: `linear-gradient(180deg, ${BASE44_COLORS.surface} 0%, ${BASE44_COLORS.background} 100%)`,
  borderRadius: 16,
  padding: 40,
  borderBottom: `3px solid ${BASE44_COLORS.orange}`,
}}>
  {children}
</div>
```

## Video Specs by Platform

| Platform | Dimensions | Duration | FPS |
|----------|------------|----------|-----|
| LinkedIn | 1920x1080 (16:9) | 15-60s | 30 |
| X/Twitter | 1920x1080 or 1080x1080 | 10-30s | 30 |
| LinkedIn Carousel | 1080x1080 (1:1) | N/A | N/A |

## Output Settings

```typescript
// remotion.config.ts
export default {
  codec: 'h264',
  imageFormat: 'jpeg',
  pixelFormat: 'yuv420p',
  audioBitrate: '320k',
};
```

## Workflow: Post → Video

1. **Write post** using `/linkedin-post` or `/x-post`
2. **Extract key elements**:
   - Feature name / headline
   - Key benefit (one line)
   - Screen recording needed (yes/no)
   - Success story details (if applicable)
3. **Select template** based on content type
4. **Generate video** with Remotion
5. **Output** to `/Users/oferbl/Desktop/Dev/Base44 Research/output/videos/`

## Example: Gmail Integration Video

**Post content:**
> Gmail just dropped for Base44
> read, send, receive emails
> Yuval built a full PA app for Maor

**Video config:**
```typescript
const GmailFeatureVideo = () => (
  <FeatureAnnouncement
    featureName="Gmail Integration"
    tagline="read. send. receive. one click."
    screenRecording="./assets/gmail-demo.mp4"
    benefit="Build CRMs, PA tools, productivity hubs"
  />
);
```
