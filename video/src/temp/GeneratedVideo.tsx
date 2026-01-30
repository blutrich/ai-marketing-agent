import { AbsoluteFill, Sequence, spring, interpolate, useCurrentFrame, useVideoConfig, Img, staticFile } from "remotion";
import { loadFont } from "@remotion/google-fonts/Inter";

const { fontFamily } = loadFont();

const Title: React.FC<{ text: string; delay?: number }> = ({ text, delay = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const animationFrame = Math.max(0, frame - delay);
  
  const scale = spring({
    frame: animationFrame,
    fps,
    config: { damping: 20, stiffness: 100 }
  });

  const opacity = interpolate(animationFrame, [0, 20], [0, 1], { extrapolateRight: "clamp" });

  return (
    <div style={{
      fontSize: 80,
      fontWeight: 800,
      color: "#000000",
      fontFamily,
      transform: `scale(${scale})`,
      opacity,
      maxWidth: "90%",
      lineHeight: 1.2
    }}>
      {text}
    </div>
  );
};

const Subtitle: React.FC<{ text: string; delay?: number }> = ({ text, delay = 0 }) => {
  const frame = useCurrentFrame();
  const animationFrame = Math.max(0, frame - delay);
  
  const opacity = interpolate(animationFrame, [0, 25], [0, 1], { extrapolateRight: "clamp" });
  const translateY = interpolate(animationFrame, [0, 25], [30, 0], { extrapolateRight: "clamp" });

  return (
    <div style={{
      fontSize: 40,
      fontWeight: 600,
      color: "#000000",
      fontFamily,
      opacity,
      transform: `translateY(${translateY}px)`,
      maxWidth: "85%",
      lineHeight: 1.4
    }}>
      {text}
    </div>
  );
};

const Highlight: React.FC<{ text: string; delay?: number }> = ({ text, delay = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const animationFrame = Math.max(0, frame - delay);
  
  const scale = spring({
    frame: animationFrame,
    fps,
    config: { damping: 15, stiffness: 120 }
  });

  return (
    <div style={{
      fontSize: 60,
      fontWeight: 700,
      color: "#FF983B",
      fontFamily,
      transform: `scale(${scale})`,
      padding: "20px 40px",
      backgroundColor: "rgba(255, 152, 59, 0.1)",
      borderRadius: 20,
      maxWidth: "85%"
    }}>
      {text}
    </div>
  );
};

const Scene1: React.FC = () => {
  const frame = useCurrentFrame();
  const logoOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: "clamp" });
  const logoScale = spring({ frame, fps: 30, config: { damping: 20 } });

  return (
    <AbsoluteFill style={{
      background: "linear-gradient(135deg, #E8F4F8 0%, #FDF5F0 100%)",
      justifyContent: "center",
      alignItems: "center",
      textAlign: "center"
    }}>
      <div style={{ opacity: logoOpacity, transform: `scale(${logoScale})`, marginBottom: 40 }}>
        <Img src={staticFile("base44_logo.jpeg")} style={{ width: 100, height: 100, borderRadius: 50 }} />
      </div>
      <Title text="Ship AI Agents" delay={15} />
      <div style={{ height: 30 }} />
      <Subtitle text="to Production in Minutes" delay={30} />
    </AbsoluteFill>
  );
};

const Scene2: React.FC = () => {
  return (
    <AbsoluteFill style={{
      background: "linear-gradient(135deg, #E8F4F8 0%, #FDF5F0 100%)",
      justifyContent: "center",
      alignItems: "center",
      textAlign: "center",
      gap: 50
    }}>
      <Title text="Anthropic Agent SDK" delay={0} />
      <Subtitle text="Deploy on Railway" delay={20} />
    </AbsoluteFill>
  );
};

const Scene3: React.FC = () => {
  return (
    <AbsoluteFill style={{
      background: "linear-gradient(135deg, #E8F4F8 0%, #FDF5F0 100%)",
      justifyContent: "center",
      alignItems: "center",
      textAlign: "center",
      gap: 50
    }}>
      <Title text="Remotion Video Skill" delay={0} />
      <Subtitle text="Generate videos programmatically" delay={20} />
    </AbsoluteFill>
  );
};

const Scene4: React.FC = () => {
  return (
    <AbsoluteFill style={{
      background: "linear-gradient(135deg, #E8F4F8 0%, #FDF5F0 100%)",
      justifyContent: "center",
      alignItems: "center",
      textAlign: "center",
      gap: 50
    }}>
      <Highlight text="Slack Bot Integration" delay={0} />
      <Subtitle text="Chat with your agent" delay={25} />
    </AbsoluteFill>
  );
};

const Scene5: React.FC = () => {
  return (
    <AbsoluteFill style={{
      background: "linear-gradient(135deg, #E8F4F8 0%, #FDF5F0 100%)",
      justifyContent: "center",
      alignItems: "center",
      textAlign: "center",
      gap: 50
    }}>
      <Title text="Production Ready" delay={0} />
      <Subtitle text="Scale without limits" delay={20} />
    </AbsoluteFill>
  );
};

const Scene6: React.FC = () => {
  const frame = useCurrentFrame();
  const logoOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: "clamp" });
  const logoScale = spring({ frame, fps: 30, config: { damping: 20 } });

  return (
    <AbsoluteFill style={{
      background: "linear-gradient(135deg, #E8F4F8 0%, #FDF5F0 100%)",
      justifyContent: "center",
      alignItems: "center",
      textAlign: "center",
      gap: 40
    }}>
      <div style={{ opacity: logoOpacity, transform: `scale(${logoScale})` }}>
        <Img src={staticFile("base44_logo.jpeg")} style={{ width: 100, height: 100, borderRadius: 50 }} />
      </div>
      <Title text="Start Building Today" delay={15} />
      <Subtitle text="base44.ai" delay={35} />
    </AbsoluteFill>
  );
};

export const GeneratedVideo: React.FC = () => {
  return (
    <AbsoluteFill>
      <Sequence from={0} durationInFrames={150}>
        <Scene1 />
      </Sequence>
      <Sequence from={150} durationInFrames={150}>
        <Scene2 />
      </Sequence>
      <Sequence from={300} durationInFrames={150}>
        <Scene3 />
      </Sequence>
      <Sequence from={450} durationInFrames={150}>
        <Scene4 />
      </Sequence>
      <Sequence from={600} durationInFrames={150}>
        <Scene5 />
      </Sequence>
      <Sequence from={750} durationInFrames={150}>
        <Scene6 />
      </Sequence>
    </AbsoluteFill>
  );
};
