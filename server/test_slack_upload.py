#!/usr/bin/env python3
"""Test uploading a video to Slack."""

import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Load from environment
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")

def upload_video_to_slack(file_path: str, channel: str, title: str = "Video"):
    """Upload a video file to Slack."""
    client = WebClient(token=SLACK_BOT_TOKEN)

    try:
        # Use files_upload_v2 for larger files
        response = client.files_upload_v2(
            channel=channel,
            file=file_path,
            title=title,
            initial_comment=f"Here's your video: {title}"
        )
        print(f"✅ Video uploaded successfully!")
        print(f"   File ID: {response['file']['id']}")
        return response
    except SlackApiError as e:
        print(f"❌ Error uploading: {e.response['error']}")
        raise

if __name__ == "__main__":
    import sys

    if not SLACK_BOT_TOKEN:
        print("❌ Set SLACK_BOT_TOKEN environment variable")
        sys.exit(1)

    # Test with a video file
    video_path = "../video/out/test.mp4"

    if not os.path.exists(video_path):
        print(f"❌ Video not found at {video_path}")
        print("   Run: cd ../video && npx remotion render Base44SpeedSimplicity out/test.mp4")
        sys.exit(1)

    # Get your Slack user ID for DM test
    # You can find this in Slack: click your profile > ... > Copy member ID
    channel = input("Enter Slack channel ID or your user ID for DM: ").strip()

    upload_video_to_slack(video_path, channel, "Test Base44 Video")
