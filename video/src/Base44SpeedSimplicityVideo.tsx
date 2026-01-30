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

// Base44 brand colors (CORRECT - from brand-system.md)
const colors = {
  // Backgrounds - light gradient
  bgTop: "#E8F4F8",      // Light blue
  bgBottom: "#FDF5F0",   // Cream/peach
  bgCard: "#FFFFFF",     // White cards
  bgSecondary: "#F0F0F0", // Light gray

  // Orange accent palette
  orange: "#FF983B",      // Primary accent
  orangeLight: "#FFE9DF", // Light accent
  orangeMedium: "#FFBFA1", // Medium accent
  orangeDark: "#EA6020",  // Dark accent

  // Text colors
  text: "#000000",        // Primary text - true black
  textSecondary: "#666666", // Secondary text
  textMuted: "#999999",   // Muted text

  // Legacy (for dark scenes only - use sparingly)
  darkBg: "#0a0a0a",
  darkText: "#FFFFFF",
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

// Scene 1: Hook - "Building apps used to take months"
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
            fontSize: 96,
            fontWeight: 700,
            color: colors.textSecondary,
            margin: 0,
            opacity: textReveal,
            lineHeight: 1.2,
          }}
        >
          Building apps
        </h2>
        <h2
          style={{
            fontSize: 96,
            fontWeight: 700,
            color: colors.text,
            margin: 0,
            marginTop: 20,
            opacity: secondLineReveal,
            lineHeight: 1.2,
          }}
        >
          used to take <span style={{ color: colors.orange }}>months</span>
        </h2>
      </div>
    </AbsoluteFill>
  );
};

// Scene 2: Pain - Code complexity visual
const PainScene = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const fadeIn = spring({
    frame,
    fps,
    config: { damping: 200 },
  });

  const codeLines = [
    "import React from 'react';",
    "import { useState, useEffect } from 'react';",
    "const MyApp = () => {",
    "  const [data, setData] = useState([]);",
    "  useEffect(() => {",
    "    fetch('/api/data')",
    "      .then(res => res.json())",
    "  }, []);",
    "  // ... 1000+ more lines",
  ];

  const visibleLines = Math.floor(
    interpolate(frame, [10, 50], [0, codeLines.length], { extrapolateRight: "clamp" })
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
      <div style={{ opacity: fadeIn, width: "100%", maxWidth: 1200 }}>
        {/* Code window - white card with shadow */}
        <div
          style={{
            background: colors.bgCard,
            borderRadius: 24,
            overflow: "hidden",
            boxShadow: "0 4px 24px rgba(0,0,0,0.08)",
          }}
        >
          <div
            style={{
              padding: "20px 30px",
              background: colors.bgSecondary,
              borderBottom: "1px solid #e0e0e0",
              fontSize: 24,
              color: colors.textSecondary,
            }}
          >
            app.tsx
          </div>
          <div
            style={{
              padding: 40,
              fontFamily: "monospace",
              fontSize: 28,
              color: colors.textSecondary,
              minHeight: 400,
            }}
          >
            {codeLines.slice(0, visibleLines).map((line, i) => (
              <div key={i} style={{ marginBottom: 8 }}>
                {line}
              </div>
            ))}
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

// Scene 3: Transition - "Not anymore"
const TransitionScene = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spring({
    frame,
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
      }}
    >
      <h2
        style={{
          fontSize: 120,
          fontWeight: 800,
          color: colors.orange,
          margin: 0,
          transform: `scale(${scale})`,
        }}
      >
        Not anymore.
      </h2>
    </AbsoluteFill>
  );
};

// Scene 4: Solution - Base44 intro with logo
const SolutionScene = () => {
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
            transform: `scale(${logoScale})`,
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
            fontSize: 52,
            color: colors.textSecondary,
            opacity: textFade,
            margin: 0,
            lineHeight: 1.4,
          }}
        >
          The AI app builder
        </p>
      </div>
    </AbsoluteFill>
  );
};

// Scene 5: Demo - Just describe what you want
const DemoScene = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const message = "Build me a CRM for real estate agents";
  const typedChars = Math.floor(
    interpolate(frame, [20, 90], [0, message.length], { extrapolateRight: "clamp" })
  );
  const displayText = message.slice(0, typedChars);

  const cursorBlink = Math.floor(frame / 15) % 2 === 0;
  const showCursor = typedChars < message.length || cursorBlink;

  const inputFade = spring({
    frame,
    fps,
    config: { damping: 200 },
  });

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
      <div style={{ opacity: inputFade, width: "100%", maxWidth: 1200 }}>
        {/* Prompt input */}
        <div
          style={{
            background: "#ffffff",
            borderRadius: 24,
            padding: "40px 50px",
            boxShadow: "0 8px 40px rgba(0,0,0,0.12)",
            border: "3px solid #e0e0e0",
            fontSize: 42,
            color: "#1a1a1a",
            fontWeight: 500,
            minHeight: 120,
            display: "flex",
            alignItems: "center",
          }}
        >
          {displayText}
          {showCursor && (
            <span
              style={{
                display: "inline-block",
                width: 4,
                height: 48,
                background: colors.orange,
                marginLeft: 4,
                verticalAlign: "middle",
              }}
            />
          )}
        </div>
        <p
          style={{
            fontSize: 28,
            color: colors.textDim,
            textAlign: "center",
            marginTop: 40,
          }}
        >
          Just describe what you want
        </p>
      </div>
    </AbsoluteFill>
  );
};

// Scene 6: Magic - Base44 builds it
const MagicScene = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const steps = [
    { icon: "🎨", text: "Designs your UI" },
    { icon: "⚡", text: "Writes the code" },
    { icon: "🗄️", text: "Sets up database" },
    { icon: "🚀", text: "Deploys your app" },
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
        {steps.map((step, i) => {
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
                padding: 40,
                boxShadow: "0 4px 24px rgba(0,0,0,0.08)",
              }}
            >
              <div style={{ fontSize: 72 }}>{step.icon}</div>
              <p
                style={{
                  fontSize: 36,
                  fontWeight: 600,
                  color: colors.text,
                  margin: 0,
                  textAlign: "center",
                }}
              >
                {step.text}
              </p>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// Scene 7: Speed reveal - "In minutes, not months"
const SpeedScene = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const firstLine = spring({
    frame,
    fps,
    config: { damping: 200 },
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
            fontSize: 88,
            fontWeight: 700,
            color: colors.text,
            margin: 0,
            opacity: firstLine,
            lineHeight: 1.3,
          }}
        >
          In <span style={{ color: colors.orange }}>minutes</span>,
        </h2>
        <h2
          style={{
            fontSize: 88,
            fontWeight: 700,
            color: colors.textSecondary,
            margin: 0,
            marginTop: 20,
            transform: `scale(${secondLine})`,
            lineHeight: 1.3,
          }}
        >
          not months
        </h2>
      </div>
    </AbsoluteFill>
  );
};

// Scene 8: CTA - "Start building today"
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
            fontSize: 96,
            fontWeight: 800,
            color: colors.text,
            margin: 0,
            opacity: textFade,
            lineHeight: 1.2,
          }}
        >
          Start building <span style={{ color: colors.orange }}>today</span>
        </h2>
        <p
          style={{
            fontSize: 44,
            color: colors.textSecondary,
            marginTop: 40,
            opacity: textFade,
          }}
        >
          No coding required
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
      </div>
    </AbsoluteFill>
  );
};

// Main Video Component
export const Base44SpeedSimplicityVideo = () => {
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ background: `linear-gradient(180deg, ${colors.bgTop} 0%, ${colors.bgBottom} 100%)` }}>
      {/* Scene 1: Hook - Building apps took months (0-3s) */}
      <Sequence from={0} durationInFrames={3 * fps} premountFor={fps}>
        <HookScene />
      </Sequence>

      {/* Scene 2: Pain - Code complexity (3-5.5s) */}
      <Sequence from={3 * fps} durationInFrames={2.5 * fps} premountFor={fps}>
        <PainScene />
      </Sequence>

      {/* Scene 3: Transition - Not anymore (5.5-7s) */}
      <Sequence from={5.5 * fps} durationInFrames={1.5 * fps} premountFor={fps}>
        <TransitionScene />
      </Sequence>

      {/* Scene 4: Solution - Base44 intro (7-10s) */}
      <Sequence from={7 * fps} durationInFrames={3 * fps} premountFor={fps}>
        <SolutionScene />
      </Sequence>

      {/* Scene 5: Demo - Type prompt (10-15s) */}
      <Sequence from={10 * fps} durationInFrames={5 * fps} premountFor={fps}>
        <DemoScene />
      </Sequence>

      {/* Scene 6: Magic - What Base44 does (15-20s) */}
      <Sequence from={15 * fps} durationInFrames={5 * fps} premountFor={fps}>
        <MagicScene />
      </Sequence>

      {/* Scene 7: Speed - Minutes not months (20-23s) */}
      <Sequence from={20 * fps} durationInFrames={3 * fps} premountFor={fps}>
        <SpeedScene />
      </Sequence>

      {/* Scene 8: CTA - Start building (23-30s) */}
      <Sequence from={23 * fps} premountFor={fps}>
        <CTAScene />
      </Sequence>
    </AbsoluteFill>
  );
};
