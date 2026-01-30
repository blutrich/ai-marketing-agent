#!/usr/bin/env python3
"""
Upload rendered video to Slack.

Usage:
    SLACK_BOT_TOKEN=xoxb-... python upload_to_slack.py <channel_id> [video_path]

Example:
    SLACK_BOT_TOKEN=xoxb-123... python upload_to_slack.py C0123456789 out/test.mp4
"""

import os
import sys

def main():
    token = os.getenv("SLACK_BOT_TOKEN")
    if not token:
        print("❌ Set SLACK_BOT_TOKEN environment variable")
        print("   SLACK_BOT_TOKEN=xoxb-... python upload_to_slack.py <channel>")
        sys.exit(1)

    if len(sys.argv) < 2:
        print("Usage: python upload_to_slack.py <channel_id> [video_path]")
        print("  channel_id: Slack channel ID (e.g., C0123456789) or user ID for DM")
        print("  video_path: Path to video file (default: out/test.mp4)")
        sys.exit(1)

    channel = sys.argv[1]
    video_path = sys.argv[2] if len(sys.argv) > 2 else "out/test.mp4"

    if not os.path.exists(video_path):
        print(f"❌ Video not found: {video_path}")
        sys.exit(1)

    file_size = os.path.getsize(video_path) / (1024 * 1024)
    print(f"📹 Video: {video_path} ({file_size:.1f} MB)")
    print(f"📤 Uploading to channel: {channel}")

    try:
        from slack_sdk import WebClient
        from slack_sdk.errors import SlackApiError

        client = WebClient(token=token)

        response = client.files_upload_v2(
            channel=channel,
            file=video_path,
            title="Base44 Video",
            initial_comment="🎬 Here's your Base44 video!"
        )

        print(f"✅ Upload successful!")
        print(f"   File ID: {response['file']['id']}")

    except ImportError:
        print("❌ slack_sdk not installed. Run: pip install slack_sdk")
        sys.exit(1)
    except SlackApiError as e:
        print(f"❌ Slack error: {e.response['error']}")
        sys.exit(1)

if __name__ == "__main__":
    main()
