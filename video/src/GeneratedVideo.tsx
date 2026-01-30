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
  bgTop: "#E8F4F8",
  bgBottom: "#FDF5F0",
  bgCard: "#FFFFFF",
  bgSecondary: "#F0F0F0",
  orange: "#FF983B",
  orangeLight: "#FFE9DF",
  orangeDark: "#EA6020",
  text: "#000000",
  textSecondary: "#666666",
  textMuted: "#999999",
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

// Scene 1: Hook - "Your phone. Your ideas."
const HookScene = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const textReveal = spring({
    frame,
    fps,
    config: { damping: 200 },
  });

  const secondLineReveal = spring({
    frame: frame - 15,
    fps,
    config: { damping: 200 },
  });

  return (
    <AbsoluteFill
      style={{
        background: `linear-gradient(180deg, ${colors.bgTop} 0%, ${colors.bgBottom} 100%)`,
        justifyContent: "center",
        alignItems: "center",
        fontFamily,
        padding: 80,
      }}
    >
      <div style={{ textAlign: "center" }}>
        <h2
          style={{
            fontSize: 120,
            fontWeight: 800,
            color: colors.orange,
            margin: 0,
            opacity: textReveal,
            lineHeight: 1.2,
          }}
        >
          Your phone.
        </h2>
        <h2
          style={{
            fontSize: 120,
            fontWeight: 800,
            color: colors.text,
            margin: 0,
            marginTop: 20,
            opacity: secondLineReveal,
            lineHeight: 1.2,
          }}
        >
          Your ideas.
        </h2>
      </div>
    </AbsoluteFill>
  );
};

// Scene 2: iOS App Reveal - "Base44 iOS is here"
const AppRevealScene = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const logoScale = spring({
    frame,
    fps,
    config: { damping: 12, stiffness: 100 },
  });

  const textFade = spring({
    frame: frame - 20,
    fps,
    config: { damping: 200 },
  });

  const pulseScale = interpolate(
    Math.sin((frame / fps) * Math.PI * 2),
    [-1, 1],
    [0.98, 1.02]
  );

  return (
    <AbsoluteFill
      style={{
        background: `linear-gradient(180deg, ${colors.bgTop} 0%, ${colors.bgBottom} 100%)`,
        justifyContent: "center",
        alignItems: "center",
        fontFamily,
        padding: 80,
      }}
    >
      <div style={{ textAlign: "center" }}>
        <div
          style={{
            transform: `scale(${logoScale * pulseScale})`,
            marginBottom: 60,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: 30,
          }}
        >
          <Base44Logo size={140} />
          <span
            style={{
              fontSize: 80,
              fontWeight: 700,
              color: colors.text,
            }}
          >
            Base44
          </span>
        </div>
        <p
          style={{
            fontSize: 64,
            fontWeight: 700,
            color: colors.text,
            opacity: textFade,
            margin: 0,
            lineHeight: 1.4,
          }}
        >
          <span style={{ color: colors.orange }}>iOS</span> is here
        </p>
        <p
          style={{
            fontSize: 40,
            color: colors.textSecondary,
            opacity: textFade,
            margin: 0,
            marginTop: 20,
            lineHeight: 1.4,
          }}
        >
          Build from anywhere
        </p>
      </div>
    </AbsoluteFill>
  );
};

// Scene 3: Location Cards - "At the gym. On the beach. While running."
const LocationScene = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const locations = [
    { emoji: "🏋️", text: "At the gym", subtitle: "Between sets" },
    { emoji: "🏖️", text: "On the beach", subtitle: "Under the sun" },
    { emoji: "🏃", text: "While running", subtitle: "On the move" },
  ];

  return (
    <AbsoluteFill
      style={{
        background: `linear-gradient(180deg, ${colors.bgTop} 0%, ${colors.bgBottom} 100%)`,
        justifyContent: "center",
        alignItems: "center",
        fontFamily,
        padding: 80,
      }}
    >
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr",
          gap: 30,
          maxWidth: 900,
          width: "100%",
        }}
      >
        {locations.map((location, i) => {
          const delay = i * 20;
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
                transform: `translateX(${translateX}px)`,
                opacity,
                background: colors.bgCard,
                borderLeft: `6px solid ${colors.orange}`,
                borderRadius: 20,
                padding: "40px 50px",
                boxShadow: "0 4px 24px rgba(0,0,0,0.08)",
              }}
            >
              <div style={{ fontSize: 80 }}>{location.emoji}</div>
              <div>
                <p
                  style={{
                    fontSize: 52,
                    fontWeight: 700,
                    color: colors.text,
                    margin: 0,
                    lineHeight: 1.2,
                  }}
                >
                  {location.text}
                </p>
                <p
                  style={{
                    fontSize: 32,
                    color: colors.textSecondary,
                    margin: 0,
                    marginTop: 8,
                    lineHeight: 1.2,
                  }}
                >
                  {location.subtitle}
                </p>
              </div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// Scene 4: Power Statement - "Full power. Zero limits."
const PowerScene = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const firstLine = spring({
    frame,
    fps,
    config: { damping: 15, stiffness: 120 },
  });

  const secondLine = spring({
    frame: frame - 20,
    fps,
    config: { damping: 15, stiffness: 120 },
  });

  return (
    <AbsoluteFill
      style={{
        background: `linear-gradient(180deg, ${colors.bgTop} 0%, ${colors.bgBottom} 100%)`,
        justifyContent: "center",
        alignItems: "center",
        fontFamily,
        padding: 80,
      }}
    >
      <div style={{ textAlign: "center" }}>
        <h2
          style={{
            fontSize: 100,
            fontWeight: 800,
            color: colors.text,
            margin: 0,
            transform: `scale(${firstLine})`,
            lineHeight: 1.3,
          }}
        >
          Full <span style={{ color: colors.orange }}>power</span>.
        </h2>
        <h2
          style={{
            fontSize: 100,
            fontWeight: 800,
            color: colors.text,
            margin: 0,
            marginTop: 20,
            transform: `scale(${secondLine})`,
            lineHeight: 1.3,
          }}
        >
          Zero limits.
        </h2>
      </div>
    </AbsoluteFill>
  );
};

// Scene 5: Feature Grid - What you can do
const FeatureScene = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const features = [
    { icon: "💬", text: "Chat with AI" },
    { icon: "🎨", text: "Design apps" },
    { icon: "⚡", text: "Ship instantly" },
    { icon: "📊", text: "Track builds" },
  ];

  return (
    <AbsoluteFill
      style={{
        background: `linear-gradient(180deg, ${colors.bgTop} 0%, ${colors.bgBottom} 100%)`,
        justifyContent: "center",
        alignItems: "center",
        fontFamily,
        padding: 80,
      }}
    >
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: 40,
          maxWidth: 1200,
        }}
      >
        {features.map((feature, i) => {
          const delay = i * 12;
          const entrance = spring({
            frame: frame - delay,
            fps,
            config: { damping: 15, stiffness: 100 },
          });

          const translateY = interpolate(entrance, [0, 1], [30, 0]);
          const opacity = entrance;

          return (
            <div
              key={i}
              style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                gap: 20,
                transform: `translateY(${translateY}px)`,
                opacity,
                background: colors.bgCard,
                borderLeft: `4px solid ${colors.orange}`,
                borderRadius: 16,
                padding: 50,
                boxShadow: "0 4px 24px rgba(0,0,0,0.08)",
              }}
            >
              <div style={{ fontSize: 80 }}>{feature.icon}</div>
              <p
                style={{
                  fontSize: 40,
                  fontWeight: 600,
                  color: colors.text,
                  margin: 0,
                  textAlign: "center",
                }}
              >
                {feature.text}
              </p>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// Scene 6: Mobile First - "Built for your pocket"
const MobileFirstScene = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const textFade = spring({
    frame,
    fps,
    config: { damping: 200 },
  });

  const phoneFloat = interpolate(
    Math.sin((frame / fps) * Math.PI * 1.5),
    [-1, 1],
    [-10, 10]
  );

  return (
    <AbsoluteFill
      style={{
        background: `linear-gradient(180deg, ${colors.bgTop} 0%, ${colors.bgBottom} 100%)`,
        justifyContent: "center",
        alignItems: "center",
        fontFamily,
        padding: 80,
      }}
    >
      <div style={{ textAlign: "center" }}>
        <div
          style={{
            fontSize: 180,
            marginBottom: 40,
            transform: `translateY(${phoneFloat}px)`,
          }}
        >
          📱
        </div>
        <h2
          style={{
            fontSize: 88,
            fontWeight: 800,
            color: colors.text,
            margin: 0,
            opacity: textFade,
            lineHeight: 1.3,
          }}
        >
          Built for your <span style={{ color: colors.orange }}>pocket</span>
        </h2>
        <p
          style={{
            fontSize: 44,
            color: colors.textSecondary,
            marginTop: 30,
            opacity: textFade,
          }}
        >
          The full Base44 experience on iOS
        </p>
      </div>
    </AbsoluteFill>
  );
};

// Scene 7: CTA - "Download now"
const CTAScene = () => {
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
        background: `linear-gradient(180deg, ${colors.bgTop} 0%, ${colors.bgBottom} 100%)`,
        justifyContent: "center",
        alignItems: "center",
        fontFamily,
        padding: 80,
      }}
    >
      <div style={{ textAlign: "center" }}>
        <h2
          style={{
            fontSize: 110,
            fontWeight: 800,
            color: colors.text,
            margin: 0,
            opacity: textFade,
            lineHeight: 1.2,
          }}
        >
          Download <span style={{ color: colors.orange }}>now</span>
        </h2>
        <p
          style={{
            fontSize: 48,
            color: colors.textSecondary,
            marginTop: 30,
            opacity: textFade,
          }}
        >
          Base44 for iOS
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
          <Base44Logo size={100} />
          <span
            style={{
              fontSize: 64,
              fontWeight: 700,
              color: colors.text,
            }}
          >
            Base44
          </span>
        </div>

        <p
          style={{
            fontSize: 36,
            color: colors.textMuted,
            marginTop: 40,
            opacity: textFade,
          }}
        >
          🍎 App Store
        </p>
      </div>
    </AbsoluteFill>
  );
};

// Main Video Component
export const GeneratedVideo = () => {
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ background: `linear-gradient(180deg, ${colors.bgTop} 0%, ${colors.bgBottom} 100%)` }}>
      {/* Scene 1: Hook - Your phone, your ideas (0-2.5s) */}
      <Sequence from={0} durationInFrames={2.5 * fps} premountFor={fps}>
        <HookScene />
      </Sequence>

      {/* Scene 2: iOS App Reveal (2.5-6s) */}
      <Sequence from={2.5 * fps} durationInFrames={3.5 * fps} premountFor={fps}>
        <AppRevealScene />
      </Sequence>

      {/* Scene 3: Locations - Gym, Beach, Running (6-11s) */}
      <Sequence from={6 * fps} durationInFrames={5 * fps} premountFor={fps}>
        <LocationScene />
      </Sequence>

      {/* Scene 4: Power Statement (11-14s) */}
      <Sequence from={11 * fps} durationInFrames={3 * fps} premountFor={fps}>
        <PowerScene />
      </Sequence>

      {/* Scene 5: Features Grid (14-19s) */}
      <Sequence from={14 * fps} durationInFrames={5 * fps} premountFor={fps}>
        <FeatureScene />
      </Sequence>

      {/* Scene 6: Mobile First (19-23s) */}
      <Sequence from={19 * fps} durationInFrames={4 * fps} premountFor={fps}>
        <MobileFirstScene />
      </Sequence>

      {/* Scene 7: CTA - Download now (23-30s) */}
      <Sequence from={23 * fps} premountFor={fps}>
        <CTAScene />
      </Sequence>
    </AbsoluteFill>
  );
};
