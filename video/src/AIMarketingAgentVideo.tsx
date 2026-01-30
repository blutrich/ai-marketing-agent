import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
  Sequence,
} from "remotion";
import { loadFont } from "@remotion/google-fonts/Inter";

const { fontFamily } = loadFont("normal", {
  weights: ["400", "600", "700", "800"],
  subsets: ["latin"],
});

// Color palette
const colors = {
  bg: "#0f0f23",
  bgGradient: "linear-gradient(135deg, #0f0f23 0%, #1a1a3e 100%)",
  primary: "#6366f1",
  secondary: "#8b5cf6",
  accent: "#22d3ee",
  text: "#ffffff",
  textMuted: "#94a3b8",
  success: "#22c55e",
};

// Scene 1: Title Card
const TitleScene = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleScale = spring({
    frame,
    fps,
    config: { damping: 12, stiffness: 100 },
  });

  const subtitleOpacity = spring({
    frame: frame - 15,
    fps,
    config: { damping: 200 },
  });

  const glowOpacity = interpolate(frame, [0, 30, 60], [0, 0.8, 0.4], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        background: colors.bgGradient,
        justifyContent: "center",
        alignItems: "center",
        fontFamily,
      }}
    >
      {/* Glow effect */}
      <div
        style={{
          position: "absolute",
          width: 600,
          height: 600,
          borderRadius: "50%",
          background: `radial-gradient(circle, ${colors.primary}40 0%, transparent 70%)`,
          opacity: glowOpacity,
          filter: "blur(60px)",
        }}
      />

      <div style={{ transform: `scale(${titleScale})`, textAlign: "center" }}>
        <h1
          style={{
            fontSize: 120,
            fontWeight: 800,
            color: colors.text,
            margin: 0,
            letterSpacing: -2,
          }}
        >
          AI Marketing
        </h1>
        <h1
          style={{
            fontSize: 120,
            fontWeight: 800,
            background: `linear-gradient(90deg, ${colors.primary}, ${colors.accent})`,
            WebkitBackgroundClip: "text",
            WebkitTextFillColor: "transparent",
            margin: 0,
            letterSpacing: -2,
          }}
        >
          Agent
        </h1>
      </div>

      <p
        style={{
          position: "absolute",
          bottom: 200,
          fontSize: 36,
          color: colors.textMuted,
          opacity: subtitleOpacity,
          fontWeight: 400,
        }}
      >
        Skills-based content generation system
      </p>
    </AbsoluteFill>
  );
};

// Scene 2: Problem Statement
const ProblemScene = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const textOpacity = spring({
    frame,
    fps,
    config: { damping: 200 },
  });

  const lineWidth = interpolate(frame, [20, 50], [0, 100], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        background: colors.bgGradient,
        justifyContent: "center",
        alignItems: "center",
        fontFamily,
      }}
    >
      <div style={{ textAlign: "center", opacity: textOpacity }}>
        <p
          style={{
            fontSize: 32,
            color: colors.accent,
            fontWeight: 600,
            marginBottom: 20,
            textTransform: "uppercase",
            letterSpacing: 4,
          }}
        >
          The Problem
        </p>
        <h2
          style={{
            fontSize: 72,
            fontWeight: 700,
            color: colors.text,
            maxWidth: 1200,
            lineHeight: 1.2,
          }}
        >
          Creating marketing content
          <br />
          <span style={{ color: colors.textMuted }}>is slow & inconsistent</span>
        </h2>
        <div
          style={{
            width: `${lineWidth}%`,
            height: 4,
            background: `linear-gradient(90deg, ${colors.primary}, ${colors.accent})`,
            margin: "40px auto",
            borderRadius: 2,
          }}
        />
      </div>
    </AbsoluteFill>
  );
};

// Skill Card Component
const SkillCard = ({
  name,
  description,
  delay,
  index,
}: {
  name: string;
  description: string;
  delay: number;
  index: number;
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({
    frame: frame - delay,
    fps,
    config: { damping: 15, stiffness: 100 },
  });

  const translateX = interpolate(entrance, [0, 1], [100, 0]);
  const opacity = entrance;

  const icons = ["", "", "", "", "", "", ""];

  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        gap: 20,
        padding: "20px 30px",
        background: "rgba(255,255,255,0.05)",
        borderRadius: 16,
        border: "1px solid rgba(255,255,255,0.1)",
        transform: `translateX(${translateX}px)`,
        opacity,
        marginBottom: 16,
      }}
    >
      <div
        style={{
          width: 50,
          height: 50,
          borderRadius: 12,
          background: `linear-gradient(135deg, ${colors.primary}, ${colors.secondary})`,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontSize: 24,
        }}
      >
        {icons[index] || ""}
      </div>
      <div>
        <h3
          style={{
            fontSize: 28,
            fontWeight: 700,
            color: colors.text,
            margin: 0,
          }}
        >
          {name}
        </h3>
        <p
          style={{
            fontSize: 18,
            color: colors.textMuted,
            margin: 0,
          }}
        >
          {description}
        </p>
      </div>
    </div>
  );
};

// Scene 3: Skills Showcase
const SkillsScene = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleOpacity = spring({
    frame,
    fps,
    config: { damping: 200 },
  });

  const skills = [
    { name: "LinkedIn Viral", description: "Hooks & engagement patterns" },
    { name: "Direct Response", description: "THE SLIDE framework emails" },
    { name: "SEO Content", description: "Search-optimized articles" },
    { name: "Landing Pages", description: "8-Section Framework" },
    { name: "GEO Content", description: "AI citation optimization" },
    { name: "Brand Voice", description: "Consistent tone across all content" },
  ];

  return (
    <AbsoluteFill
      style={{
        background: colors.bgGradient,
        fontFamily,
        padding: 80,
      }}
    >
      <div style={{ display: "flex", gap: 80 }}>
        {/* Left side - Title */}
        <div style={{ flex: 1, opacity: titleOpacity }}>
          <p
            style={{
              fontSize: 24,
              color: colors.accent,
              fontWeight: 600,
              textTransform: "uppercase",
              letterSpacing: 4,
              marginBottom: 20,
            }}
          >
            Powered by Skills
          </p>
          <h2
            style={{
              fontSize: 64,
              fontWeight: 800,
              color: colors.text,
              lineHeight: 1.1,
              marginBottom: 30,
            }}
          >
            7 Specialized
            <br />
            <span
              style={{
                background: `linear-gradient(90deg, ${colors.primary}, ${colors.accent})`,
                WebkitBackgroundClip: "text",
                WebkitTextFillColor: "transparent",
              }}
            >
              Content Skills
            </span>
          </h2>
          <p
            style={{
              fontSize: 24,
              color: colors.textMuted,
              lineHeight: 1.6,
            }}
          >
            Each skill is a specialized expert for a specific content type.
          </p>
        </div>

        {/* Right side - Skills list */}
        <div style={{ flex: 1 }}>
          {skills.map((skill, i) => (
            <SkillCard
              key={skill.name}
              name={skill.name}
              description={skill.description}
              delay={i * 8}
              index={i}
            />
          ))}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// Scene 4: API Demo
const APIScene = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const codeOpacity = spring({
    frame,
    fps,
    config: { damping: 200 },
  });

  const cursorBlink = Math.floor(frame / 15) % 2 === 0;

  const codeLines = [
    'curl -X POST /generate-content \\',
    '  -H "Content-Type: application/json" \\',
    '  -d \'{"content_type": "linkedin",',
    '       "prompt": "AI trends for 2024"}\'',
  ];

  const responseLines = [
    '{',
    '  "content": "AI is transforming how we...",',
    '  "hooks": ["Did you know?", "Here\'s why..."],',
    '  "engagement_tips": [...]',
    '}',
  ];

  const visibleCodeLines = Math.min(
    Math.floor(interpolate(frame, [10, 60], [0, codeLines.length])),
    codeLines.length
  );

  const showResponse = frame > 80;
  const visibleResponseLines = showResponse
    ? Math.min(
        Math.floor(interpolate(frame, [80, 120], [0, responseLines.length])),
        responseLines.length
      )
    : 0;

  return (
    <AbsoluteFill
      style={{
        background: colors.bgGradient,
        fontFamily,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <div style={{ textAlign: "center", marginBottom: 40, opacity: codeOpacity }}>
        <p
          style={{
            fontSize: 24,
            color: colors.accent,
            fontWeight: 600,
            textTransform: "uppercase",
            letterSpacing: 4,
          }}
        >
          Simple API
        </p>
        <h2
          style={{
            fontSize: 56,
            fontWeight: 800,
            color: colors.text,
          }}
        >
          One Request, Expert Content
        </h2>
      </div>

      <div
        style={{
          display: "flex",
          gap: 40,
          opacity: codeOpacity,
        }}
      >
        {/* Request */}
        <div
          style={{
            background: "#1e1e3f",
            borderRadius: 16,
            padding: 30,
            minWidth: 600,
            border: "1px solid rgba(255,255,255,0.1)",
          }}
        >
          <div
            style={{
              display: "flex",
              gap: 8,
              marginBottom: 20,
            }}
          >
            <div style={{ width: 12, height: 12, borderRadius: 6, background: "#ff5f56" }} />
            <div style={{ width: 12, height: 12, borderRadius: 6, background: "#ffbd2e" }} />
            <div style={{ width: 12, height: 12, borderRadius: 6, background: "#27ca40" }} />
          </div>
          <pre
            style={{
              fontFamily: "monospace",
              fontSize: 20,
              color: colors.accent,
              margin: 0,
              lineHeight: 1.6,
            }}
          >
            {codeLines.slice(0, visibleCodeLines).join("\n")}
            {visibleCodeLines < codeLines.length && cursorBlink && (
              <span style={{ background: colors.accent, color: colors.bg }}>_</span>
            )}
          </pre>
        </div>

        {/* Response */}
        {showResponse && (
          <div
            style={{
              background: "#1e1e3f",
              borderRadius: 16,
              padding: 30,
              minWidth: 500,
              border: `1px solid ${colors.success}40`,
            }}
          >
            <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 20 }}>
              <div
                style={{
                  width: 10,
                  height: 10,
                  borderRadius: 5,
                  background: colors.success,
                }}
              />
              <span style={{ color: colors.success, fontSize: 16, fontWeight: 600 }}>
                200 OK
              </span>
            </div>
            <pre
              style={{
                fontFamily: "monospace",
                fontSize: 18,
                color: colors.success,
                margin: 0,
                lineHeight: 1.6,
              }}
            >
              {responseLines.slice(0, visibleResponseLines).join("\n")}
            </pre>
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};

// Scene 5: CTA
const CTAScene = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spring({
    frame,
    fps,
    config: { damping: 10, stiffness: 80 },
  });

  const buttonPulse = interpolate(
    Math.sin(frame * 0.1),
    [-1, 1],
    [1, 1.05]
  );

  return (
    <AbsoluteFill
      style={{
        background: colors.bgGradient,
        fontFamily,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <div style={{ textAlign: "center", transform: `scale(${scale})` }}>
        <h2
          style={{
            fontSize: 80,
            fontWeight: 800,
            color: colors.text,
            marginBottom: 20,
          }}
        >
          Start Creating
        </h2>
        <h2
          style={{
            fontSize: 80,
            fontWeight: 800,
            background: `linear-gradient(90deg, ${colors.primary}, ${colors.accent})`,
            WebkitBackgroundClip: "text",
            WebkitTextFillColor: "transparent",
            marginBottom: 60,
          }}
        >
          Better Content
        </h2>

        <div
          style={{
            display: "inline-block",
            padding: "24px 60px",
            background: `linear-gradient(90deg, ${colors.primary}, ${colors.secondary})`,
            borderRadius: 16,
            transform: `scale(${buttonPulse})`,
          }}
        >
          <span
            style={{
              fontSize: 32,
              fontWeight: 700,
              color: colors.text,
            }}
          >
            AI Marketing Agent
          </span>
        </div>
      </div>
    </AbsoluteFill>
  );
};

// Main Video Component
export const AIMarketingAgentVideo = () => {
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ background: colors.bg }}>
      {/* Scene 1: Title (0-3s) */}
      <Sequence from={0} durationInFrames={3 * fps} premountFor={fps}>
        <TitleScene />
      </Sequence>

      {/* Scene 2: Problem (3-6s) */}
      <Sequence from={3 * fps} durationInFrames={3 * fps} premountFor={fps}>
        <ProblemScene />
      </Sequence>

      {/* Scene 3: Skills (6-11s) */}
      <Sequence from={6 * fps} durationInFrames={5 * fps} premountFor={fps}>
        <SkillsScene />
      </Sequence>

      {/* Scene 4: API (11-15s) */}
      <Sequence from={11 * fps} durationInFrames={4 * fps} premountFor={fps}>
        <APIScene />
      </Sequence>

      {/* Scene 5: CTA (15-15s) */}
      <Sequence from={11 * fps + 4 * fps} premountFor={fps}>
        <CTAScene />
      </Sequence>
    </AbsoluteFill>
  );
};
