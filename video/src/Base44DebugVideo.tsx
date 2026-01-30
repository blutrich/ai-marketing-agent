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
  red: "#ef4444",
  green: "#22c55e",
};

// Base44 Logo Component using actual image
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

// Scene 1: The Problem - App not working (MOBILE OPTIMIZED)
const ProblemScene = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const fadeIn = spring({
    frame,
    fps,
    config: { damping: 200 },
  });

  const glitchOffset = Math.sin(frame * 0.5) * 3;
  const showError = frame > 30;

  const errorShake = showError
    ? Math.sin(frame * 2) * interpolate(frame, [30, 50], [5, 0], { extrapolateRight: "clamp" })
    : 0;

  return (
    <AbsoluteFill
      style={{
        background: colors.bg,
        justifyContent: "center",
        alignItems: "center",
        fontFamily,
        padding: 40,
      }}
    >
      {/* Browser mockup - bigger for mobile */}
      <div
        style={{
          width: "100%",
          maxWidth: 950,
          background: colors.bgCard,
          borderRadius: 24,
          overflow: "hidden",
          opacity: fadeIn,
          transform: `translateX(${errorShake}px)`,
          border: "2px solid #333",
        }}
      >
        {/* Browser header */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            padding: "20px 24px",
            background: "#1a1a1a",
            gap: 12,
          }}
        >
          <div style={{ width: 18, height: 18, borderRadius: 9, background: "#ff5f56" }} />
          <div style={{ width: 18, height: 18, borderRadius: 9, background: "#ffbd2e" }} />
          <div style={{ width: 18, height: 18, borderRadius: 9, background: "#27ca40" }} />
          <div
            style={{
              marginLeft: 30,
              padding: "10px 60px",
              background: "#0a0a0a",
              borderRadius: 8,
              fontSize: 20,
              color: colors.textMuted,
            }}
          >
            your-app.com
          </div>
        </div>

        {/* App content - broken state */}
        <div
          style={{
            padding: 60,
            minHeight: 400,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          {!showError ? (
            <div style={{ display: "flex", gap: 12 }}>
              <div
                style={{
                  width: 20,
                  height: 20,
                  borderRadius: 10,
                  background: colors.orange,
                  opacity: (frame % 30) < 10 ? 1 : 0.3,
                }}
              />
              <div
                style={{
                  width: 20,
                  height: 20,
                  borderRadius: 10,
                  background: colors.orange,
                  opacity: (frame % 30) >= 10 && (frame % 30) < 20 ? 1 : 0.3,
                }}
              />
              <div
                style={{
                  width: 20,
                  height: 20,
                  borderRadius: 10,
                  background: colors.orange,
                  opacity: (frame % 30) >= 20 ? 1 : 0.3,
                }}
              />
            </div>
          ) : (
            <div style={{ textAlign: "center" }}>
              <div
                style={{
                  fontSize: 100,
                  marginBottom: 30,
                  transform: `translateX(${glitchOffset}px)`,
                }}
              >
                😕
              </div>
              <p
                style={{
                  fontSize: 36,
                  color: colors.textMuted,
                  margin: 0,
                }}
              >
                Something went wrong
              </p>
              <p
                style={{
                  fontSize: 24,
                  color: colors.textDim,
                  marginTop: 16,
                }}
              >
                No error details available
              </p>
            </div>
          )}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// Scene 2: The Frustration (MOBILE OPTIMIZED)
const FrustrationScene = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const textReveal = spring({
    frame,
    fps,
    config: { damping: 200 },
  });

  const secondLine = spring({
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
        padding: 60,
      }}
    >
      <div style={{ textAlign: "center" }}>
        <h2
          style={{
            fontSize: 80,
            fontWeight: 700,
            color: colors.text,
            margin: 0,
            opacity: textReveal,
            lineHeight: 1.3,
          }}
        >
          The hardest part?
        </h2>
        <h2
          style={{
            fontSize: 80,
            fontWeight: 700,
            color: colors.textMuted,
            margin: 0,
            marginTop: 20,
            opacity: secondLine,
            lineHeight: 1.3,
          }}
        >
          Figuring out <span style={{ color: colors.red }}>why</span>
        </h2>
      </div>
    </AbsoluteFill>
  );
};

// Scene 3: No Clear Error (MOBILE OPTIMIZED)
const NoErrorScene = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const fadeIn = spring({
    frame,
    fps,
    config: { damping: 200 },
  });

  const consoleLogs = [
    { type: "log", text: "[App] Initializing..." },
    { type: "log", text: "[App] Loading data..." },
    { type: "log", text: "[App] Rendering..." },
    { type: "warn", text: "[Warning] Unexpected" },
    { type: "log", text: "[App] ???" },
  ];

  const visibleLogs = Math.floor(
    interpolate(frame, [10, 70], [0, consoleLogs.length], { extrapolateRight: "clamp" })
  );

  return (
    <AbsoluteFill
      style={{
        background: colors.bg,
        justifyContent: "center",
        alignItems: "center",
        fontFamily,
        padding: 50,
      }}
    >
      <div style={{ opacity: fadeIn, width: "100%" }}>
        <p
          style={{
            fontSize: 28,
            color: colors.orange,
            fontWeight: 600,
            textTransform: "uppercase",
            letterSpacing: 4,
            marginBottom: 50,
            textAlign: "center",
          }}
        >
          No clear error
        </p>

        {/* Console mockup - bigger for mobile */}
        <div
          style={{
            width: "100%",
            maxWidth: 900,
            margin: "0 auto",
            background: "#1a1a1a",
            borderRadius: 20,
            overflow: "hidden",
            border: "2px solid #333",
          }}
        >
          <div
            style={{
              padding: "16px 24px",
              background: "#222",
              fontSize: 22,
              color: colors.textMuted,
              borderBottom: "2px solid #333",
            }}
          >
            Console
          </div>
          <div style={{ padding: 30, fontFamily: "monospace", fontSize: 26 }}>
            {consoleLogs.slice(0, visibleLogs).map((log, i) => (
              <div
                key={i}
                style={{
                  color: log.type === "warn" ? "#fbbf24" : colors.textMuted,
                  marginBottom: 8,
                }}
              >
                {log.text}
              </div>
            ))}
            {visibleLogs >= consoleLogs.length && (
              <div
                style={{
                  color: colors.textDim,
                  marginTop: 20,
                  fontStyle: "italic",
                }}
              >
                No errors in console...
              </div>
            )}
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

// Scene 4: The Solution - Just tell Base44 (MOBILE OPTIMIZED)
const SolutionScene = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const logoScale = spring({
    frame,
    fps,
    config: { damping: 12, stiffness: 100 },
  });

  const textFade = spring({
    frame: frame - 15,
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
        padding: 60,
      }}
    >
      <div style={{ textAlign: "center" }}>
        <div style={{ transform: `scale(${logoScale})`, marginBottom: 60 }}>
          <Base44Logo size={160} />
        </div>
        <p
          style={{
            fontSize: 48,
            color: colors.textMuted,
            opacity: textFade,
            margin: 0,
            lineHeight: 1.4,
          }}
        >
          Now, you can just tell Base44:
        </p>
      </div>
    </AbsoluteFill>
  );
};

// Scene 5: Type "something is wrong" - using real Base44 prompt bar (MOBILE OPTIMIZED)
const TypeScene = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const message = "something is wrong";
  const typedChars = Math.floor(
    interpolate(frame, [20, 80], [0, message.length], { extrapolateRight: "clamp" })
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
        background: "#e8eaed",
        justifyContent: "center",
        alignItems: "center",
        fontFamily,
        padding: 40,
      }}
    >
      <div style={{ opacity: inputFade, position: "relative", width: "100%" }}>
        {/* Real Base44 prompt bar image - scaled for mobile */}
        <Img
          src={staticFile("base44-prompt-bar.png")}
          style={{
            width: "100%",
            maxWidth: 980,
            margin: "0 auto",
            display: "block",
            borderRadius: 20,
            boxShadow: "0 8px 40px rgba(0,0,0,0.15)",
          }}
        />
        {/* Typing overlay positioned on the input area */}
        <div
          style={{
            position: "absolute",
            top: 36,
            left: 80,
            fontSize: 28,
            fontWeight: 400,
            color: "#1a1a1a",
            fontFamily: "system-ui, -apple-system, sans-serif",
          }}
        >
          {displayText}
          {showCursor && (
            <span
              style={{
                display: "inline-block",
                width: 3,
                height: 32,
                background: colors.orange,
                marginLeft: 2,
                verticalAlign: "middle",
              }}
            />
          )}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// Scene 6: The Magic - We handle it (MOBILE OPTIMIZED - vertical layout)
const MagicScene = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const steps = [
    { icon: "🔍", text: "Gather context" },
    { icon: "🎯", text: "Pinpoint what happened" },
    { icon: "✨", text: "Help you fix it" },
  ];

  return (
    <AbsoluteFill
      style={{
        background: colors.bg,
        justifyContent: "center",
        alignItems: "center",
        fontFamily,
        padding: 60,
      }}
    >
      <div style={{ display: "flex", flexDirection: "column", gap: 50 }}>
        {steps.map((step, i) => {
          const delay = i * 15;
          const entrance = spring({
            frame: frame - delay,
            fps,
            config: { damping: 15, stiffness: 100 },
          });

          const translateY = interpolate(entrance, [0, 1], [40, 0]);
          const opacity = entrance;

          return (
            <div
              key={i}
              style={{
                display: "flex",
                alignItems: "center",
                gap: 30,
                transform: `translateY(${translateY}px)`,
                opacity,
              }}
            >
              <div
                style={{
                  width: 140,
                  height: 140,
                  borderRadius: 32,
                  background: `linear-gradient(135deg, ${colors.orange}20, ${colors.orange}10)`,
                  border: `3px solid ${colors.orange}40`,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontSize: 64,
                  flexShrink: 0,
                }}
              >
                {step.icon}
              </div>
              <p
                style={{
                  fontSize: 42,
                  fontWeight: 600,
                  color: colors.text,
                  margin: 0,
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

// Scene 7: No explanation needed (MOBILE OPTIMIZED)
const NoExplanationScene = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const textFade = spring({
    frame,
    fps,
    config: { damping: 200 },
  });

  const strikeWidth = interpolate(frame, [30, 50], [0, 100], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        background: colors.bg,
        justifyContent: "center",
        alignItems: "center",
        fontFamily,
        padding: 60,
      }}
    >
      <div style={{ textAlign: "center", opacity: textFade }}>
        <div style={{ position: "relative", display: "inline-block" }}>
          <h2
            style={{
              fontSize: 72,
              fontWeight: 700,
              color: colors.textDim,
              margin: 0,
              lineHeight: 1.3,
            }}
          >
            No explanation
            <br />
            needed
          </h2>
          <div
            style={{
              position: "absolute",
              top: "50%",
              left: 0,
              width: `${strikeWidth}%`,
              height: 6,
              background: colors.orange,
              transform: "translateY(-50%)",
            }}
          />
        </div>
      </div>
    </AbsoluteFill>
  );
};

// Scene 8: CTA - Less guessing, more shipping (MOBILE OPTIMIZED)
const CTAScene = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const line1 = spring({
    frame,
    fps,
    config: { damping: 15, stiffness: 100 },
  });

  const line2 = spring({
    frame: frame - 15,
    fps,
    config: { damping: 15, stiffness: 100 },
  });

  const logoFade = spring({
    frame: frame - 40,
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
        padding: 60,
      }}
    >
      <div style={{ textAlign: "center" }}>
        <h2
          style={{
            fontSize: 86,
            fontWeight: 700,
            color: colors.textMuted,
            margin: 0,
            transform: `scale(${line1})`,
            lineHeight: 1.2,
          }}
        >
          Less guessing.
        </h2>
        <h2
          style={{
            fontSize: 86,
            fontWeight: 800,
            color: colors.text,
            margin: 0,
            marginTop: 20,
            transform: `scale(${line2})`,
            lineHeight: 1.2,
          }}
        >
          More <span style={{ color: colors.orange }}>shipping</span>.
        </h2>

        <div
          style={{
            marginTop: 100,
            opacity: logoFade,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: 24,
          }}
        >
          <Base44Logo size={80} />
          <span
            style={{
              fontSize: 56,
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
export const Base44DebugVideo = () => {
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ background: colors.bg }}>
      {/* Scene 1: Problem - App broken (0-2s) */}
      <Sequence from={0} durationInFrames={2.5 * fps} premountFor={fps}>
        <ProblemScene />
      </Sequence>

      {/* Scene 2: Frustration (2.5-5s) */}
      <Sequence from={2.5 * fps} durationInFrames={2.5 * fps} premountFor={fps}>
        <FrustrationScene />
      </Sequence>

      {/* Scene 3: No clear error (5-8s) */}
      <Sequence from={5 * fps} durationInFrames={3 * fps} premountFor={fps}>
        <NoErrorScene />
      </Sequence>

      {/* Scene 4: Solution intro (8-10s) */}
      <Sequence from={8 * fps} durationInFrames={2 * fps} premountFor={fps}>
        <SolutionScene />
      </Sequence>

      {/* Scene 5: Type "something is wrong" (10-13s) */}
      <Sequence from={10 * fps} durationInFrames={3.5 * fps} premountFor={fps}>
        <TypeScene />
      </Sequence>

      {/* Scene 6: Magic steps (13.5-17s) */}
      <Sequence from={13.5 * fps} durationInFrames={3.5 * fps} premountFor={fps}>
        <MagicScene />
      </Sequence>

      {/* Scene 7: No explanation needed (17-19s) */}
      <Sequence from={17 * fps} durationInFrames={2 * fps} premountFor={fps}>
        <NoExplanationScene />
      </Sequence>

      {/* Scene 8: CTA (19-22s) */}
      <Sequence from={19 * fps} premountFor={fps}>
        <CTAScene />
      </Sequence>
    </AbsoluteFill>
  );
};
