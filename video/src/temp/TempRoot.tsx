import { Composition } from "remotion";
import { TestVideo } from "./TestVideo";

export const TempRoot = () => {
  return (
    <Composition
      id="TestVideo"
      component={TestVideo}
      durationInFrames={300}
      fps={30}
      width={1920}
      height={1080}
    />
  );
};
