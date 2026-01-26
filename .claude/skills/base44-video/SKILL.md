---
name: base44-video
description: Generate Remotion videos from Base44 social posts
metadata:
  tags: base44, video, remotion, linkedin, x, social
---

# Base44 Video Generator

Transform Base44 social posts into Remotion video compositions.

## When to Use

Use this skill AFTER creating a post with `/linkedin-post` or `/x-post`. This skill takes that content and generates a matching video.

## Workflow

```
/linkedin-post or /x-post → write post → /base44-video → generate video code
```

## Step 1: Identify Post Type

| Post Content | Video Template | Duration |
|--------------|----------------|----------|
| Feature announcement (new drop) | `FeatureAnnouncement` | 15-30s |
| Success story (builder highlight) | `SuccessStory` | 30-60s |
| Quick update / stat | `QuickDemo` | 10-20s |
| Enterprise story ($350K, etc.) | `ImpactStory` | 20-30s |
| Playful / game demo | `PlayfulBuild` | 20-40s |

## Step 2: Extract Video Elements

From the post, extract:

1. **Headline** - The main hook or announcement (first line usually)
2. **Key stat** - Any number ($350K, $1M ARR, 30 days, etc.)
3. **Benefit line** - What it enables (one sentence)
4. **Builder name** - If success story (optional)
5. **CTA** - Closing action (optional)

## Step 3: Generate Remotion Composition

### For Feature Announcements

```typescript
// src/compositions/[FeatureName].tsx
import { AbsoluteFill, Sequence, useCurrentFrame, useVideoConfig, spring, interpolate } from 'remotion';
import { BASE44_COLORS, BASE44_FONTS } from '../styles';

export const [FeatureName]Video: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ backgroundColor: BASE44_COLORS.background }}>
      {/* Scene 1: Logo (0-2s) */}
      <Sequence from={0} durationInFrames={2 * fps}>
        <LogoIntro />
      </Sequence>

      {/* Scene 2: Headline (2-6s) */}
      <Sequence from={2 * fps} durationInFrames={4 * fps}>
        <HeadlineReveal text="[HEADLINE FROM POST]" />
      </Sequence>

      {/* Scene 3: Key benefit (6-12s) */}
      <Sequence from={6 * fps} durationInFrames={6 * fps}>
        <BenefitText text="[BENEFIT LINE FROM POST]" />
      </Sequence>

      {/* Scene 4: CTA (12-15s) */}
      <Sequence from={12 * fps}>
        <CTASlide text="[CTA FROM POST]" />
      </Sequence>
    </AbsoluteFill>
  );
};
```

### For Success Stories

```typescript
export const [BuilderName]Story: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ backgroundColor: BASE44_COLORS.background }}>
      {/* Scene 1: Big number hook (0-4s) */}
      <Sequence from={0} durationInFrames={4 * fps}>
        <BigNumberReveal number="[STAT]" label="[CONTEXT]" />
      </Sequence>

      {/* Scene 2: Builder intro (4-10s) */}
      <Sequence from={4 * fps} durationInFrames={6 * fps}>
        <BuilderIntro name="[NAME]" product="[PRODUCT]" />
      </Sequence>

      {/* Scene 3: The shift (10-18s) */}
      <Sequence from={10 * fps} durationInFrames={8 * fps}>
        <ShiftMoment before="[BEFORE]" after="[AFTER]" />
      </Sequence>

      {/* Scene 4: CTA (18-20s) */}
      <Sequence from={18 * fps}>
        <CTASlide />
      </Sequence>
    </AbsoluteFill>
  );
};
```

### For Quick Stats / Impact

```typescript
export const ImpactVideo: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ backgroundColor: BASE44_COLORS.background }}>
      {/* Scene 1: Stat punch (0-3s) */}
      <Sequence from={0} durationInFrames={3 * fps}>
        <StatPunch stat="$350K" context="Salesforce contract" action="terminated" />
      </Sequence>

      {/* Scene 2: Replacement (3-6s) */}
      <Sequence from={3 * fps} durationInFrames={3 * fps}>
        <ReplacedWith text="Custom solution on Base44" />
      </Sequence>

      {/* Scene 3: Frequency (6-9s) */}
      <Sequence from={6 * fps} durationInFrames={3 * fps}>
        <TextReveal text="Happening weekly now" />
      </Sequence>

      {/* Scene 4: Tagline (9-12s) */}
      <Sequence from={9 * fps}>
        <Tagline text="Builders aren't waiting anymore" />
      </Sequence>
    </AbsoluteFill>
  );
};
```

## Step 4: Register Composition

Add to `src/Root.tsx`:

```typescript
import { Composition } from 'remotion';
import { [VideoName] } from './compositions/[VideoName]';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="[video-name]"
        component={[VideoName]}
        durationInFrames={[duration] * 30}
        fps={30}
        width={1920}
        height={1080}
      />
    </>
  );
};
```

## Step 5: Output

Generate files to:
```
/Users/oferbl/Desktop/Dev/Base44 Research/remotion-videos/src/compositions/
```

## Brand Components (Pre-built)

Reference these from `src/components/`:

| Component | Purpose |
|-----------|---------|
| `<LogoIntro />` | Base44 logo with orange pulse animation |
| `<HeadlineReveal text="" />` | Big text with slide-up reveal |
| `<TextReveal text="" />` | Standard text animation |
| `<BigNumberReveal number="" label="" />` | Animated stat counter |
| `<StatPunch stat="" context="" />` | Impact number with context |
| `<CTASlide text="" />` | Closing CTA with logo |
| `<GradientBg />` | Cream-to-orange gradient background |
| `<DarkCard />` | Dark card with orange bottom border |

## Example: Salesforce Post → Video

**Post:**
> Just heard of a customer that terminated a $350K contract with Salesforce for a custom solution they built on top of Base44.
> I've been getting these stories on a weekly basis now.
> Something's shifting. Builders aren't waiting for vendors anymore.

**Extracted:**
- Headline: "$350K Salesforce contract terminated"
- Stat: $350K
- Benefit: "Replaced with custom Base44 solution"
- Frequency: "Weekly basis"
- Tagline: "Builders aren't waiting anymore"

**Video:** 12-second `ImpactStory` template

## Render Command

```bash
cd /Users/oferbl/Desktop/Dev/Base44 Research/remotion-videos
npx remotion render [composition-id] out/[name].mp4
```

---

## Brand Data Loading

When generating Base44 videos, load brand data for accurate stats and voice:

**Required reads:**
- `Read: /app/brands/base44/tone-of-voice.md` - Voice and vocabulary rules
- `Read: /app/brands/base44/facts/metrics.md` - Current stats and numbers

**For success stories:**
- `Read: /app/brands/base44/case-studies/index.md` - Quick reference of all cases

**For Remotion rules:**
- `Read: ../remotion/rules/` - Remotion best practices
