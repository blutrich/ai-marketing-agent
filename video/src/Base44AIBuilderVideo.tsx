import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
  Sequence,
  Img,
  staticFile,
} from "remotion";
import { loadFont } from "@remotion/google-fonts/Inter";

const { fontFamily } = loadFont("normal", {
  weights: ["400", "500", "600", "700", "800"],
  subsets: ["latin"],
});

// Base44 brand colors
const colors = {
  bg: "#0a0a0a",
  bgCard: "#141414",
  orange: "#ff6b35",
  orangeLight: "#ff8c5a",
  text: "#ffffff",
  textMuted: "#888888",
  textDim: "#555555",
  cream: "#fef9f3",
};

// Base44 Logo Component
const Base44Logo = ({ size = 60 }: { size?: number }) => {
  return (
    <Img
      src={staticFile("base44_logo.jpeg")}
      style={{
        width: size,
        height: size,
        borderRadius: size / 2,
        objectFit: "cover",
      }}
    />
  );
};

// Scene 1: Logo Intro with pulse
const LogoIntro = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const logoScale = spring({
    frame,
    fps,
    config: { damping: 12, stiffness: 100 },
  });

  const pulseScale = 1 + Math.sin(frame / 10) * 0.05;

  return (
    <AbsoluteFill
      style={{
        background: colors.bg,
        justifyContent: "center",
        alignItems: "center",
        fontFamily,
      }}
    >
      <div
        style={{
          transform: `scale(${logoScale * pulseScale})`,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 30,
        }}
      >
        <Base44Logo size={180} />
        <span
          style={{
            fontSize: 72,
            fontWeight: 700,
            color: colors.text,
          }}
        >
          Base44
        </span>
      </div>
    </AbsoluteFill>
  );
};

// Scene 2: Headline Reveal - "The AI App Builder"
const HeadlineReveal = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const line1 = spring({
    frame,
    fps,
    config: { damping: 200 },
  });

  const line2 = spring({
    frame: frame - 15,
    fps,
    config: { damping: 200 },
  });

  const translateY1 = interpolate(line1, [0, 1], [50, 0]);
  const translateY2 = interpolate(line2, [0, 1], [50, 0]);

  return (
    <AbsoluteFill
      style={{
        background: colors.bg,
        justifyContent: "center",
        alignItems: "center",
        fontFamily,
        padding: 80,
      }}
    >
      <div style={{ textAlign: "center" }}>
        <h1
          style={{
            fontSize: 120,
            fontWeight: 800,
            color: colors.orange,
            margin: 0,
            opacity: line1,
            transform: `translateY(${translateY1}px)`,
            lineHeight: 1.1,
          }}
        >
          The AI App Builder
        </h1>
        <p
          style={{
            fontSize: 56,
            color: colors.textMuted,
            marginTop: 40,
            opacity: line2,
            transform: `translateY(${translateY2}px)`,
            margin: 0,
            marginTop: 40,
          }}
        >
          That actually works
        </p>
      </div>
    </AbsoluteFill>
  );
};

// Scene 3: Benefit Text with animated cards
const BenefitCards = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const benefits = [
    { emoji: "💭", text: "Describe your idea" },
    { emoji: "⚡", text: "AI builds it instantly" },
    { emoji: "🚀", text: "Launch in minutes" },
  ];

  return (
    <AbsoluteFill
      style={{
        background: colors.cream,
        justifyContent: "center",
        alignItems: "center",
        fontFamily,
        padding: 80,
      }}
    >
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: 40,
          width: "100%",
          maxWidth: 1200,
        }}
      >
        {benefits.map((benefit, i) => {
          const delay = i * 15;
          const entrance = spring({
            frame: frame - delay,
            fps,
            config: { damping: 15, stiffness: 100 },
          });

          const translateX = interpolate(entrance, [0, 1], [-100, 0]);
          const opacity = entrance;

          return (
            <div
              key={i}
              style={{
                display: "flex",
                alignItems: "center",
                gap: 40,
                background: "#ffffff",
                borderRadius: 24,
                padding: "40px 60px",
                boxShadow: "0 8px 40px rgba(0,0,0,0.12)",
                border: `3px solid ${colors.orange}`,
                transform: `translateX(${translateX}px)`,
                opacity,
              }}
            >
              <div style={{ fontSize: 80 }}>{benefit.emoji}</div>
              <p
                style={{
                  fontSize: 52,
                  fontWeight: 600,
                  color: "#1a1a1a",
                  margin: 0,
                }}
              >
                {benefit.text}
              </p>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// Scene 4: Big Stat Reveal
const BigStat = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const statEntrance = spring({
    frame,
    fps,
    config: { damping: 15, stiffness: 120 },
  });

  const labelFade = spring({
    frame: frame - 20,
    fps,
    config: { damping: 200 },
  });

  return (
    <AbsoluteFill
      style={{
        background: colors.bg,
        justifyContent: "center",
        alignItems: "center",
        fontFamily,
        padding: 80,
      }}
    >
      <div style={{ textAlign: "center" }}>
        <h2
          style={{
            fontSize: 160,
            fontWeight: 800,
            color: colors.orange,
            margin: 0,
            transform: `scale(${statEntrance})`,
            lineHeight: 1,
          }}
        >
          10x
        </h2>
        <p
          style={{
            fontSize: 52,
            color: colors.textMuted,
            marginTop: 40,
            opacity: labelFade,
            margin: 0,
            marginTop: 40,
          }}
        >
          Faster than traditional development
        </p>
      </div>
    </AbsoluteFill>
  );
};

// Scene 5: CTA with Logo
const CTASlide = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const textFade = spring({
    frame,
    fps,
    config: { damping: 200 },
  });

  const logoEntrance = spring({
    frame: frame - 20,
    fps,
    config: { damping: 15, stiffness: 100 },
  });

  return (
    <AbsoluteFill
      style={{
        background: `linear-gradient(135deg, ${colors.bg} 0%, #1a1a1a 100%)`,
        justifyContent: "center",
        alignItems: "center",
        fontFamily,
        padding: 80,
      }}
    >
      <div style={{ textAlign: "center" }}>
        <h2
          style={{
            fontSize: 88,
            fontWeight: 800,
            color: colors.orange,
            margin: 0,
            opacity: textFade,
            lineHeight: 1.2,
          }}
        >
          Start building today
        </h2>
        <p
          style={{
            fontSize: 48,
            color: colors.textMuted,
            marginTop: 30,
            opacity: textFade,
            margin: 0,
            marginTop: 30,
          }}
        >
          base44.com
        </p>

        <div
          style={{
            marginTop: 80,
            transform: `scale(${logoEntrance})`,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: 30,
          }}
        >
          <Base44Logo size={120} />
        </div>
      </div>
    </AbsoluteFill>
  );
};

// Main Video Component
export const Base44AIBuilderVideo = () => {
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ background: colors.bg }}>
      {/* Scene 1: Logo Intro (0-2s) */}
      <Sequence from={0} durationInFrames={2 * fps} premountFor={1 * fps}>
        <LogoIntro />
      </Sequence>

      {/* Scene 2: Headline Reveal (2-6s) */}
      <Sequence from={2 * fps} durationInFrames={4 * fps} premountFor={1 * fps}>
        <HeadlineReveal />
      </Sequence>

      {/* Scene 3: Benefit Cards (6-15s) */}
      <Sequence from={6 * fps} durationInFrames={9 * fps} premountFor={1 * fps}>
        <BenefitCards />
      </Sequence>

      {/* Scene 4: Big Stat (15-20s) */}
      <Sequence from={15 * fps} durationInFrames={5 * fps} premountFor={1 * fps}>
        <BigStat />
      </Sequence>

      {/* Scene 5: CTA (20-30s) */}
      <Sequence from={20 * fps} premountFor={1 * fps}>
        <CTASlide />
      </Sequence>
    </AbsoluteFill>
  );
};
