"""Slack Bot for Marketing Agent.

Simple Slack integration that connects to the existing agent API.
Uses Socket Mode for easy setup (no public URL needed).
Persists user sessions in Supabase.
Supports video generation with Remotion.
"""

import os
import re
import logging
import subprocess
import tempfile
import httpx
from pathlib import Path
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

# Video project path (works both locally and in Docker)
VIDEO_PROJECT_PATH = Path(os.environ.get("VIDEO_PROJECT_PATH", Path(__file__).parent.parent / "video"))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Slack app setup
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Agent API URL (Railway deployment or local)
AGENT_API_URL = os.environ.get(
    "AGENT_API_URL",
    "https://ai-marketing-agent-production-60c7.up.railway.app"
)

# Supabase client for persisting user sessions
supabase: Client = None
try:
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_KEY")
    if supabase_url and supabase_key:
        supabase = create_client(supabase_url, supabase_key)
        logger.info("Supabase connected for session persistence")
    else:
        logger.warning("Supabase not configured - sessions won't persist across restarts")
except Exception as e:
    logger.error(f"Failed to connect to Supabase: {e}")

# Fallback in-memory storage if Supabase not available
memory_sessions: dict[str, str] = {}


def get_user_session(slack_user_id: str) -> str | None:
    """Get session ID for a Slack user."""
    if supabase:
        try:
            result = supabase.table("slack_users").select("session_id").eq(
                "slack_user_id", slack_user_id
            ).execute()
            if result.data and result.data[0].get("session_id"):
                return result.data[0]["session_id"]
        except Exception as e:
            logger.error(f"Failed to get user session: {e}")
    return memory_sessions.get(slack_user_id)


def save_user_session(slack_user_id: str, session_id: str, username: str = None):
    """Save session ID for a Slack user."""
    memory_sessions[slack_user_id] = session_id

    if supabase:
        try:
            supabase.table("slack_users").upsert({
                "slack_user_id": slack_user_id,
                "session_id": session_id,
                "slack_username": username,
                "updated_at": "now()"
            }, on_conflict="slack_user_id").execute()
        except Exception as e:
            logger.error(f"Failed to save user session: {e}")


def clear_user_session(slack_user_id: str):
    """Clear session for a Slack user."""
    if slack_user_id in memory_sessions:
        del memory_sessions[slack_user_id]

    if supabase:
        try:
            supabase.table("slack_users").update({
                "session_id": None,
                "updated_at": "now()"
            }).eq("slack_user_id", slack_user_id).execute()
        except Exception as e:
            logger.error(f"Failed to clear user session: {e}")


def call_agent(user_id: str, message: str, username: str = None) -> str:
    """Call the marketing agent API (synchronous to avoid event loop conflicts)."""
    session_id = get_user_session(user_id)

    payload = {"message": message}
    if session_id:
        payload["session_id"] = session_id

    with httpx.Client(timeout=120.0) as client:
        response = client.post(
            f"{AGENT_API_URL}/agent/chat",
            json=payload
        )
        response.raise_for_status()
        data = response.json()

        # Save session for continuity
        if "session_id" in data:
            save_user_session(user_id, data["session_id"], username)

        return data.get("content", "Sorry, I couldn't generate a response.")


def is_video_request(message: str) -> bool:
    """Check if the message is requesting a video."""
    video_keywords = [
        r'\bvideo\b', r'\bremotio?n\b', r'\banimate\b', r'\banimation\b',
        r'\bmp4\b', r'\brender\b', r'\bclip\b'
    ]
    message_lower = message.lower()
    return any(re.search(kw, message_lower) for kw in video_keywords)


def detect_content_type(message: str) -> str | None:
    """Detect content type from message keywords for skill routing."""
    message_lower = message.lower()

    patterns = {
        # Existing content types
        "linkedin": [r'\blinkedin\b', r'\blinked-in\b'],
        "email": [r'\bemail\b', r'\be-mail\b', r'\bnewsletter\b'],
        "seo": [r'\bseo\b', r'\bsearch engine\b', r'\bblog post\b', r'\barticle\b'],
        "geo": [r'\bgeo\b', r'\bai citation\b', r'\bllm discovery\b'],
        "landing-page": [r'\blanding page\b', r'\blanding-page\b', r'\bsales page\b'],
        "direct-response": [r'\bdirect response\b', r'\bsales copy\b', r'\bad copy\b'],
        # New skills
        "linkedin-post": [r'\blinkedin post\b', r'\blinkedin content\b'],
        "x-post": [r'\btweet\b', r'\btwitter\b', r'\bx post\b', r'\bx thread\b'],
        "slides": [r'\bslides?\b', r'\bpresentation\b', r'\bpptx\b', r'\bpowerpoint\b', r'\bdeck\b'],
        "diagram": [r'\bdiagram\b', r'\bflowchart\b', r'\barchitecture diagram\b', r'\bexcalidraw\b'],
        "image": [r'\bgenerate image\b', r'\bcreate image\b', r'\bmockup\b', r'\bvisual\b', r'\bimagen\b'],
        "brand-setup": [r'\bbrand system\b', r'\bbrand setup\b', r'\btone of voice\b', r'\bbrand identity\b'],
        "sop": [r'\brunbook\b', r'\bplaybook\b', r'\bsop\b', r'\bdocumentation\b', r'\bprocedure\b'],
        "skill": [r'\bcreate skill\b', r'\bnew skill\b', r'\bskill creator\b'],
    }

    for content_type, keywords in patterns.items():
        if any(re.search(kw, message_lower) for kw in keywords):
            return content_type
    return None


# Content types that need longer processing time
SLOW_CONTENT_TYPES = {"slides", "image", "seo", "diagram", "brand-setup"}

# Friendly names and emojis for content types
CONTENT_TYPE_INFO = {
    "slides": ("📊", "presentation slides", "This may take 1-2 minutes."),
    "image": ("🎨", "image", "This may take 1-2 minutes."),
    "seo": ("📝", "SEO article", "This may take 2-3 minutes for a full article."),
    "diagram": ("📐", "diagram", "This may take 1-2 minutes."),
    "brand-setup": ("🎯", "brand system", "This may take 1-2 minutes."),
}


def is_slow_content_type(content_type: str) -> bool:
    """Check if content type requires longer processing."""
    return content_type in SLOW_CONTENT_TYPES


def call_content_api(content_type: str, prompt: str, timeout: float = 120.0) -> str:
    """Call /generate-content with specific content type for skill routing."""
    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.post(
                f"{AGENT_API_URL}/generate-content",
                json={"content_type": content_type, "prompt": prompt}
            )
            response.raise_for_status()
            return response.json().get("content", "Sorry, couldn't generate content.")
    except Exception as e:
        logger.error(f"Content API error: {e}")
        raise


def generate_slow_content(client, channel: str, user_id: str, content_type: str, message: str, username: str = None, thread_ts: str = None):
    """Generate slow content types (slides, images, SEO) with longer timeout."""
    emoji, name, time_msg = CONTENT_TYPE_INFO.get(content_type, ("✍️", content_type, "This may take a moment."))

    try:
        # Use 300 second timeout for slow content
        response = call_content_api(content_type, message, timeout=300.0)

        # Check if response contains a file path (for slides/images)
        if content_type == "slides" and ".pptx" in response:
            # Extract file path and upload
            import re
            pptx_match = re.search(r'(/[^\s]+\.pptx)', response)
            if pptx_match:
                file_path = pptx_match.group(1)
                try:
                    client.files_upload_v2(
                        channel=channel,
                        thread_ts=thread_ts,
                        file=file_path,
                        title="Generated Presentation",
                        initial_comment=f"{emoji} Here's your presentation!"
                    )
                    return
                except Exception as e:
                    logger.error(f"Failed to upload PPTX: {e}")

        elif content_type == "image" and any(ext in response for ext in [".png", ".jpg", ".jpeg"]):
            # Extract image path and upload
            import re
            img_match = re.search(r'(/[^\s]+\.(png|jpg|jpeg))', response)
            if img_match:
                file_path = img_match.group(1)
                try:
                    client.files_upload_v2(
                        channel=channel,
                        thread_ts=thread_ts,
                        file=file_path,
                        title="Generated Image",
                        initial_comment=f"{emoji} Here's your image!"
                    )
                    return
                except Exception as e:
                    logger.error(f"Failed to upload image: {e}")

        # Default: just send the text response
        if thread_ts:
            client.chat_postMessage(channel=channel, thread_ts=thread_ts, text=response)
        else:
            client.chat_postMessage(channel=channel, text=response)

    except Exception as e:
        logger.error(f"Slow content generation error: {e}")
        error_msg = f"❌ Failed to generate {name}: {str(e)[:100]}"
        if thread_ts:
            client.chat_postMessage(channel=channel, thread_ts=thread_ts, text=error_msg)
        else:
            client.chat_postMessage(channel=channel, text=error_msg)


def extract_typescript_code(content: str) -> str | None:
    """Extract TypeScript code block from agent response."""
    # Look for ```typescript or ```tsx code blocks
    pattern = r'```(?:typescript|tsx)\n([\s\S]*?)```'
    matches = re.findall(pattern, content)
    if matches:
        # Return the largest code block (likely the main component)
        return max(matches, key=len)
    return None


def render_video(code: str, composition_id: str = "GeneratedVideo") -> str | None:
    """Render video from Remotion code. Returns path to rendered video."""
    if not VIDEO_PROJECT_PATH.exists():
        logger.error(f"Video project not found at {VIDEO_PROJECT_PATH}")
        return None

    try:
        # Create temp file for the composition
        temp_dir = VIDEO_PROJECT_PATH / "src" / "temp"
        temp_dir.mkdir(exist_ok=True)

        comp_file = temp_dir / f"{composition_id}.tsx"
        comp_file.write_text(code)
        logger.info(f"Wrote composition to {comp_file}")

        # Create a temporary Root.tsx that includes our composition
        # Using 900 frames (30 seconds at 30fps) to accommodate longer videos
        temp_root = temp_dir / "TempRoot.tsx"
        temp_root_content = '''import { Composition } from "remotion";
import { COMP_NAME } from "./COMP_NAME";

export const TempRoot = () => {
  return (
    <Composition
      id="COMP_NAME"
      component={COMP_NAME}
      durationInFrames={900}
      fps={30}
      width={1920}
      height={1080}
    />
  );
};
'''.replace("COMP_NAME", composition_id)
        temp_root.write_text(temp_root_content)

        # Create entry point with registerRoot (required by Remotion CLI)
        temp_index = temp_dir / "index.ts"
        temp_index.write_text(f'''
import {{ registerRoot }} from "remotion";
import {{ TempRoot }} from "./TempRoot";

registerRoot(TempRoot);
''')

        # Output path
        output_path = VIDEO_PROJECT_PATH / "out" / f"{composition_id}.mp4"
        output_path.parent.mkdir(exist_ok=True)

        # Run Remotion render (using temp/index.ts as entry point with registerRoot)
        logger.info(f"Rendering video to {output_path}...")
        logger.info(f"Working directory: {VIDEO_PROJECT_PATH}")
        logger.info(f"VIDEO_PROJECT_PATH exists: {VIDEO_PROJECT_PATH.exists()}")

        # In Docker, npx is in PATH. Locally might need nvm.
        if os.environ.get("DOCKER_ENV"):
            # Low memory mode for Railway: 720p, single-threaded
            cmd = f'npx remotion render src/temp/index.ts {composition_id} "{output_path}" --concurrency=1 --scale=0.67'
        else:
            cmd = f'source ~/.nvm/nvm.sh && npx remotion render src/temp/index.ts {composition_id} "{output_path}"'
        logger.info(f"Running command: {cmd}")

        result = subprocess.run(
            cmd,
            cwd=str(VIDEO_PROJECT_PATH),  # Convert Path to string
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
            shell=True,
            executable='/bin/bash'
        )

        logger.info(f"Subprocess completed with return code: {result.returncode}")

        if result.returncode != 0:
            logger.error(f"Remotion render failed (exit code {result.returncode})")
            logger.error(f"STDOUT: {result.stdout[:2000] if result.stdout else 'empty'}")
            logger.error(f"STDERR: {result.stderr[:2000] if result.stderr else 'empty'}")
            return None

        if output_path.exists():
            logger.info(f"Video rendered successfully: {output_path}")
            return str(output_path)
        else:
            logger.error(f"Video file not created at {output_path}")
            logger.error(f"STDOUT was: {result.stdout[:1000] if result.stdout else 'empty'}")
            return None

    except subprocess.TimeoutExpired:
        logger.error("Video rendering timed out")
        return None
    except Exception as e:
        logger.error(f"Error rendering video: {e}")
        return None


def upload_video_to_slack(client, channel: str, file_path: str, title: str = "Base44 Video") -> bool:
    """Upload video file to Slack channel."""
    try:
        response = client.files_upload_v2(
            channel=channel,
            file=file_path,
            title=title,
            initial_comment="🎬 Here's your video!"
        )
        logger.info(f"Video uploaded to Slack: {response['file']['id']}")
        return True
    except Exception as e:
        logger.error(f"Failed to upload video to Slack: {e}")
        return False


def generate_and_send_video(client, channel: str, user_id: str, message: str, username: str = None, thread_ts: str = None):
    """Generate video and send to Slack (synchronous)."""
    try:
        # Step 1: Generate video code
        video_prompt = f"""```typescript
import {{ AbsoluteFill, Sequence, spring, interpolate, useCurrentFrame, useVideoConfig, Img, staticFile }} from "remotion";
import {{ loadFont }} from "@remotion/google-fonts/Inter";

const {{ fontFamily }} = loadFont();

const colors = {{
  bgTop: "#E8F4F8",
  bgBottom: "#FDF5F0",
  text: "#000000",
  orange: "#FF983B",
}};

// Scene components here - each with centered AbsoluteFill
// Use spring({{ frame, fps, config: {{ damping: 200 }} }}) for animations
// Use <Img src={{staticFile("base44_logo.jpeg")}} style={{{{ width: 80, height: 80, borderRadius: 40 }}}} /> for logo

export const GeneratedVideo = () => {{
  const {{ fps }} = useVideoConfig();
  return (
    <AbsoluteFill style={{{{ background: "linear-gradient(180deg, #E8F4F8 0%, #FDF5F0 100%)" }}}}>
      <Sequence from={{0}} durationInFrames={{3 * fps}}>{{/* Logo intro */}}</Sequence>
      <Sequence from={{3 * fps}} durationInFrames={{21 * fps}}>{{/* Content */}}</Sequence>
      <Sequence from={{24 * fps}}>{{/* CTA with logo */}}</Sequence>
    </AbsoluteFill>
  );
}};
```

Complete the code above for this video topic: {message}

RULES:
- Output ONLY the completed TypeScript code in a ```typescript block
- NO explanations, NO Hebrew, NO commentary
- Component must be named GeneratedVideo and exported
- 30 seconds total (900 frames at 30fps)
- ALL scenes must be centered: justifyContent: "center", alignItems: "center"
- Include Base44 logo in first and last scene using staticFile("base44_logo.jpeg")
- Use spring() with {{ damping: 200 }} for smooth animations
- NO CSS animations - only useCurrentFrame() driven animations"""

        logger.info("Generating video code...")
        content = call_agent(user_id, video_prompt, username)
        logger.info(f"Agent response length: {len(content)} chars")
        logger.info(f"Agent response preview: {content[:500]}...")

        # Step 2: Extract code
        code = extract_typescript_code(content)
        logger.info(f"Extracted code: {'Yes, ' + str(len(code)) + ' chars' if code else 'No code found'}")
        if not code:
            if thread_ts:
                client.chat_postMessage(channel=channel, thread_ts=thread_ts,
                    text="❌ Couldn't generate valid video code. Here's what I got:\n\n" + content[:1000])
            else:
                client.chat_postMessage(channel=channel,
                    text="❌ Couldn't generate valid video code. Try a simpler request.")
            return

        # Step 3: Render video
        logger.info("Rendering video (this may take a minute)...")
        video_path = render_video(code, "GeneratedVideo")

        if not video_path:
            if thread_ts:
                client.chat_postMessage(channel=channel, thread_ts=thread_ts,
                    text="❌ Video rendering failed. The code was generated but couldn't be rendered.")
            else:
                client.chat_postMessage(channel=channel,
                    text="❌ Video rendering failed.")
            return

        # Step 4: Upload to Slack
        logger.info("Uploading video to Slack...")
        success = upload_video_to_slack(client, channel, video_path, "Base44 Video")

        if not success:
            if thread_ts:
                client.chat_postMessage(channel=channel, thread_ts=thread_ts,
                    text="❌ Video was rendered but upload failed.")
            else:
                client.chat_postMessage(channel=channel,
                    text="❌ Video was rendered but upload failed.")

    except Exception as e:
        logger.error(f"Video generation error: {e}")
        if thread_ts:
            client.chat_postMessage(channel=channel, thread_ts=thread_ts,
                text=f"❌ Error generating video: {str(e)[:200]}")
        else:
            client.chat_postMessage(channel=channel,
                text=f"❌ Error generating video: {str(e)[:200]}")


def get_username(client, user_id: str) -> str:
    """Get username from Slack user ID."""
    try:
        result = client.users_info(user=user_id)
        if result["ok"]:
            return result["user"]["real_name"] or result["user"]["name"]
    except Exception:
        pass
    return None


@app.event("app_mention")
def handle_mention(event, say, client):
    """Handle @MarketingBot mentions in channels."""
    user_id = event["user"]
    text = event["text"]
    channel = event["channel"]
    thread_ts = event.get("thread_ts") or event["ts"]
    username = get_username(client, user_id)

    # Remove the bot mention from the message
    message = text.split(">", 1)[-1].strip() if ">" in text else text

    if not message:
        say("Hi! How can I help with your marketing today?", thread_ts=thread_ts)
        return

    # Check if this is a video request
    if is_video_request(message):
        say("🎬 Generating video... This may take 1-2 minutes.", thread_ts=thread_ts)
        try:
            generate_and_send_video(client, channel, user_id, message, username, thread_ts)
        except Exception as e:
            logger.error(f"Video generation error: {e}")
            say(f"❌ Video generation failed: {str(e)[:100]}", thread_ts=thread_ts)
        return

    # Check for content type keywords for skill routing
    content_type = detect_content_type(message)
    if content_type:
        # Handle slow content types (slides, images, SEO) with async pattern
        if is_slow_content_type(content_type):
            emoji, name, time_msg = CONTENT_TYPE_INFO.get(content_type, ("✍️", content_type, ""))
            say(f"{emoji} Generating {name}... {time_msg}", thread_ts=thread_ts)
            try:
                generate_slow_content(client, channel, user_id, content_type, message, username, thread_ts)
            except Exception as e:
                logger.error(f"Slow content error: {e}")
                say(f"❌ Failed to generate {name}: {str(e)[:100]}", thread_ts=thread_ts)
            return

        # Fast content types
        say(f"✍️ Creating {content_type} content...", thread_ts=thread_ts)
        try:
            response = call_content_api(content_type, message)
            say(response, thread_ts=thread_ts)
        except Exception as e:
            logger.error(f"Content API error: {e}")
            say(f"Sorry, something went wrong. Please try again.", thread_ts=thread_ts)
        return

    # Regular text request (stateful chat)
    say("🤔 Thinking...", thread_ts=thread_ts)

    try:
        response = call_agent(user_id, message, username)
        say(response, thread_ts=thread_ts)
    except Exception as e:
        logger.error(f"Agent error: {e}")
        say(f"Sorry, something went wrong. Please try again.", thread_ts=thread_ts)


@app.event("message")
def handle_dm(event, say, client):
    """Handle direct messages to the bot."""
    # Ignore bot messages and channel messages
    if event.get("bot_id") or event.get("channel_type") != "im":
        return

    user_id = event["user"]
    channel = event["channel"]
    message = event.get("text", "")
    username = get_username(client, user_id)

    if not message:
        return

    # Check if this is a video request
    if is_video_request(message):
        say("🎬 Generating video... This may take 1-2 minutes.")
        try:
            generate_and_send_video(client, channel, user_id, message, username)
        except Exception as e:
            logger.error(f"Video generation error: {e}")
            say(f"❌ Video generation failed: {str(e)[:100]}")
        return

    # Check for content type keywords for skill routing
    content_type = detect_content_type(message)
    if content_type:
        # Handle slow content types (slides, images, SEO) with async pattern
        if is_slow_content_type(content_type):
            emoji, name, time_msg = CONTENT_TYPE_INFO.get(content_type, ("✍️", content_type, ""))
            say(f"{emoji} Generating {name}... {time_msg}")
            try:
                generate_slow_content(client, channel, user_id, content_type, message, username)
            except Exception as e:
                logger.error(f"Slow content error: {e}")
                say(f"❌ Failed to generate {name}: {str(e)[:100]}")
            return

        # Fast content types
        say(f"✍️ Creating {content_type} content...")
        try:
            response = call_content_api(content_type, message)
            say(response)
        except Exception as e:
            logger.error(f"Content API error: {e}")
            say("Sorry, something went wrong. Please try again.")
        return

    # Regular text request (stateful chat)
    try:
        response = call_agent(user_id, message, username)
        say(response)
    except Exception as e:
        logger.error(f"Agent error: {e}")
        say("Sorry, something went wrong. Please try again.")


@app.command("/marketing")
def handle_slash_command(ack, respond, command, client):
    """Handle /marketing slash command."""
    ack()

    user_id = command["user_id"]
    channel_id = command["channel_id"]
    message = command["text"]
    username = get_username(client, user_id)

    if not message:
        respond("Usage: `/marketing <your request>`\n\nExamples:\n• `/marketing Write a LinkedIn post about AI consulting`\n• `/marketing video about Base44 speed and simplicity`")
        return

    # Check if this is a video request
    if is_video_request(message):
        respond("🎬 Generating video... This may take 1-2 minutes. I'll post it when ready!")
        try:
            generate_and_send_video(client, channel_id, user_id, message, username)
        except Exception as e:
            logger.error(f"Video generation error: {e}")
            respond(f"❌ Video generation failed: {str(e)[:100]}")
        return

    # Check for content type keywords for skill routing
    content_type = detect_content_type(message)
    if content_type:
        # Handle slow content types (slides, images, SEO) with async pattern
        if is_slow_content_type(content_type):
            emoji, name, time_msg = CONTENT_TYPE_INFO.get(content_type, ("✍️", content_type, ""))
            respond(f"{emoji} Generating {name}... {time_msg} I'll post it when ready!")
            try:
                generate_slow_content(client, channel_id, user_id, content_type, message, username)
            except Exception as e:
                logger.error(f"Slow content error: {e}")
                respond(f"❌ Failed to generate {name}: {str(e)[:100]}")
            return

        # Fast content types
        respond(f"✍️ Creating {content_type} content...")
        try:
            response = call_content_api(content_type, message)
            respond(response)
        except Exception as e:
            logger.error(f"Content API error: {e}")
            respond("Sorry, something went wrong. Please try again.")
        return

    # Regular text request (stateful chat)
    respond("🤔 Thinking...")

    try:
        response = call_agent(user_id, message, username)
        respond(response)
    except Exception as e:
        logger.error(f"Agent error: {e}")
        respond("Sorry, something went wrong. Please try again.")


@app.command("/clear")
def handle_clear(ack, respond, command):
    """Clear conversation history for the user."""
    ack()
    user_id = command["user_id"]

    clear_user_session(user_id)
    respond("✅ Conversation cleared! I've forgotten our previous chat.")


@app.command("/video")
def handle_video_command(ack, respond, command, client):
    """Handle /video slash command for video generation."""
    ack()

    user_id = command["user_id"]
    channel_id = command["channel_id"]
    message = command["text"]
    username = get_username(client, user_id)

    if not message:
        respond("Usage: `/video <description>`\n\nExamples:\n• `/video Base44 speed and simplicity`\n• `/video $350K Salesforce contract terminated`\n• `/video AI app builder for small business`")
        return

    respond("🎬 Generating video... This may take 1-2 minutes. I'll post it when ready!")

    try:
        generate_and_send_video(client, channel_id, user_id, message, username)
    except Exception as e:
        logger.error(f"Video generation error: {e}")
        respond(f"❌ Video generation failed: {str(e)[:100]}")


if __name__ == "__main__":
    # Socket Mode uses WebSocket - no public URL needed
    handler = SocketModeHandler(
        app,
        os.environ.get("SLACK_APP_TOKEN")
    )
    logger.info("Starting Slack bot in Socket Mode...")
    handler.start()
