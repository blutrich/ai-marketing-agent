import { AbsoluteFill, Sequence, spring, interpolate, useCurrentFrame, useVideoConfig, Img, staticFile } from "remotion";
import { loadFont } from "@remotion/google-fonts/Inter";

const { fontFamily } = loadFont();

const colors = {
  bgTop: "#E8F4F8",
  bgBottom: "#FDF5F0",
  text: "#000000",
  orange: "#FF983B",
};

const LogoIntro = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spring({
    frame,
    fps,
    config: { damping: 200 },
  });

  const opacity = interpolate(frame, [0, 15], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
      <div style={{ transform: `scale(${scale})`, opacity, textAlign: "center" }}>
        <Img
          src={staticFile("base44_logo.jpeg")}
          style={{ width: 120, height: 120, borderRadius: 60 }}
        />
        <div style={{
          fontFamily,
          fontSize: 48,
          fontWeight: 700,
          color: colors.text,
          marginTop: 20
        }}>
          Base44
        </div>
      </div>
    </AbsoluteFill>
  );
};

const MainContent = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const slideIn = spring({
    frame,
    fps,
    config: { damping: 200 },
  });

  const x = interpolate(slideIn, [0, 1], [100, 0]);

  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
      <div style={{
        transform: `translateX(${x}px)`,
        textAlign: "center",
        padding: 40,
      }}>
        <div style={{
          fontFamily,
          fontSize: 64,
          fontWeight: 700,
          color: colors.text,
          marginBottom: 20,
        }}>
          Video Generation Test
        </div>
        <div style={{
          fontFamily,
          fontSize: 32,
          color: colors.orange,
        }}>
          Slack Bot + Railway
        </div>
      </div>
    </AbsoluteFill>
  );
};

const CTA = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spring({
    frame,
    fps,
    config: { damping: 200 },
  });

  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
      <div style={{ transform: `scale(${scale})`, textAlign: "center" }}>
        <Img
          src={staticFile("base44_logo.jpeg")}
          style={{ width: 80, height: 80, borderRadius: 40, marginBottom: 20 }}
        />
        <div style={{
          fontFamily,
          fontSize: 48,
          fontWeight: 700,
          color: colors.text,
        }}>
          Build with Base44
        </div>
        <div style={{
          fontFamily,
          fontSize: 24,
          color: colors.orange,
          marginTop: 10,
        }}>
          base44.com
        </div>
      </div>
    </AbsoluteFill>
  );
};

export const TestVideo = () => {
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ background: `linear-gradient(180deg, ${colors.bgTop} 0%, ${colors.bgBottom} 100%)` }}>
      <Sequence from={0} durationInFrames={3 * fps}>
        <LogoIntro />
      </Sequence>
      <Sequence from={3 * fps} durationInFrames={4 * fps}>
        <MainContent />
      </Sequence>
      <Sequence from={7 * fps} durationInFrames={3 * fps}>
        <CTA />
      </Sequence>
    </AbsoluteFill>
  );
};
