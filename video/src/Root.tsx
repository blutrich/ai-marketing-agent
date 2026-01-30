import { Composition, Folder } from "remotion";
import { AIMarketingAgentVideo } from "./AIMarketingAgentVideo";
import { Base44DebugVideo } from "./Base44DebugVideo";
import { Base44SpeedSimplicityVideo } from "./Base44SpeedSimplicityVideo";
import { Base44AIBuilderVideo } from "./Base44AIBuilderVideo";

export const RemotionRoot = () => {
  return (
    <>
      <Folder name="Base44">
        <Composition
          id="Base44Debug"
          component={Base44DebugVideo}
          durationInFrames={660}
          fps={30}
          width={1080}
          height={1920}
        />
        <Composition
          id="Base44SpeedSimplicity"
          component={Base44SpeedSimplicityVideo}
          durationInFrames={900}
          fps={30}
          width={1920}
          height={1080}
        />
        <Composition
          id="Base44AIBuilder"
          component={Base44AIBuilderVideo}
          durationInFrames={900}
          fps={30}
          width={1920}
          height={1080}
        />
      </Folder>
      <Folder name="AI-Marketing-Agent">
        <Composition
          id="AIMarketingAgent"
          component={AIMarketingAgentVideo}
          durationInFrames={450}
          fps={30}
          width={1920}
          height={1080}
        />
      </Folder>
    </>
  );
};
