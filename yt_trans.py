#!/usr/bin/env python3
# =========================
# BASIC DOCS
# =========================
# Usage: ./yt_trans.py "dQw4w9WgXcQ" or ./yt_trans.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
# Youtube really hates this. You may need to rotate your cookies.txt every few files. Assume your google account and any others on your IP will be banned.
# Requires OPENAI_API_KEY environment variable.
# Uses yt_dlp to download transcripts.
# Requires youtube cookies.txt for yt_dlp. Read yt_dlp docs for details.
# Handles youtube videos with a leading hyphen poorly.
# Requires transcript.prompt containing chatgpt promts for what to actually do with the transcript.
# My normal transcript.prompt:
## Provide a detailed summary fo the following transcript. Call out any novel concepts, philosophies, and action items.
## Call out any cognitive errors or poor reasoning use by the speakers that might be present in arguments for a conclusion, especially confirmation bias.
## This is any cognitive errors that the speaker might be using, rather than any cognitive errors the speaker is discussing.

import os
import sys
import subprocess
import glob
import re
import html
import argparse
import json
import requests

# =========================
# CONFIGURATION
# =========================
# Path or executable name for the yt-dlp tool.
YT_DLP_EXECUTABLE = "yt-dlp_macos"
# Options for downloading auto-generated subtitles (in English) without downloading the video.
YT_DLP_OPTIONS = ["--write-auto-subs", "--skip-download", "--sub-lang", "en", "--cookies", "cookies.txt"]


# Default ChatGPT model to use (can be overridden on the command line).
DEFAULT_CHATGPT_MODEL = "gpt-5-nano"

# Default prompt file to use.
DEFAULT_PROMPT_FILE = "transcript.prompt"

# =========================

def extract_video_id(input_str):
    """
    Given a YouTube URL or video id (possibly with quotes), extract the video id.
    Supports full URLs (including youtu.be links) or raw video ids.
    """
    input_str = input_str.strip('"').strip("'")
    if "youtube.com" in input_str or "youtu.be" in input_str:
        m = re.search(r"(?:v=|youtu\.be/)([\w-]+)", input_str)
        if m:
            return m.group(1)
    return input_str

def download_transcript(video_url):
    """
    Uses the yt-dlp tool to download auto-generated English subtitles.
    """
    command = [YT_DLP_EXECUTABLE] + YT_DLP_OPTIONS + [video_url]
    print("Running command: " + " ".join(command))
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print("Error running yt-dlp:")
        print(result.stderr)
        sys.exit(1)

def find_vtt_file(video_id):
    """
    Finds the .vtt file corresponding to the video by searching for the video_id in the filename.
    If multiple files are found, returns the most recently modified.
    """
    pattern = f"*{video_id}*.vtt"
    vtt_files = glob.glob(pattern)
    if not vtt_files:
        return None
    return max(vtt_files, key=os.path.getmtime)

def process_vtt_file(filename):
    """
    Reads a .vtt file, strips metadata (timestamps, cue numbers, WEBVTT header),
    removes HTML tags, unescapes HTML entities, escapes special characters,
    and removes consecutive duplicate lines.
    Returns a plain-text transcript.
    """
    output_lines = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("WEBVTT") or line.isdigit():
                continue
            if "-->" in line:
                continue
            # Remove any HTML tags if present.
            line = re.sub(r'<[^>]+>', '', line)
            # Unescape HTML entities.
            line = html.unescape(line)
            # Escape special characters (converting non-ASCII to Unicode escapes).
            line = line.encode('unicode_escape').decode('utf-8')
            output_lines.append(line)
    
    # Remove consecutive duplicate lines.
    deduped_lines = []
    for line in output_lines:
        if not deduped_lines or line != deduped_lines[-1]:
            deduped_lines.append(line)
    return "\n".join(deduped_lines)

def main():
    parser = argparse.ArgumentParser(
        description="Generate high-value ChatGPT summaries of YouTube videos by downloading auto-generated subtitles."
    )
    parser.add_argument("video", help="YouTube URL or video id (with or without quotes)")
    parser.add_argument("--model", default=DEFAULT_CHATGPT_MODEL, help="ChatGPT model to use")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT_FILE, help="Path to prompt file")
    args = parser.parse_args()

    # Extract video id and form full URL if needed.
    video_id = extract_video_id(args.video)
    if not (args.video.startswith("http://") or args.video.startswith("https://")):
        video_url = f"https://www.youtube.com/watch?v={video_id}"
    else:
        video_url = args.video

    print(f"Using video id: {video_id}")
    print(f"Video URL: {video_url}")

    # Download transcript via yt-dlp.
    download_transcript(video_url)

    # Locate the downloaded .vtt file.
    vtt_file = find_vtt_file(video_id)
    if not vtt_file:
        print("Could not locate the .vtt file for the video.")
        sys.exit(1)
    print(f"Found transcript file: {vtt_file}")

    # Process the .vtt file to extract a clean transcript.
    transcript_text = process_vtt_file(vtt_file)

    # Read the ChatGPT prompt from the specified file.
    if not os.path.exists(args.prompt):
        print(f"Prompt file {args.prompt} not found.")
        sys.exit(1)
    with open(args.prompt, 'r', encoding='utf-8') as pf:
        prompt_text = pf.read()

    # Append the transcript text to the prompt.
    full_prompt = prompt_text.strip() + "\n\n" + transcript_text

    # Verify that the OpenAI API key is set.
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Please set the OPENAI_API_KEY environment variable.")
        sys.exit(1)

    # Submit the combined prompt (original prompt + transcript) to the ChatGPT API.
    chat_url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": args.model,
        "messages": [
            {"role": "user", "content": full_prompt}
        ]
    }
    print("Submitting prompt to ChatGPT...")
    response = requests.post(chat_url, headers=headers, json=payload)
    if response.status_code != 200:
        print("Error calling ChatGPT API:", response.status_code, response.text)
        sys.exit(1)
    data = response.json()
    summary = data["choices"][0]["message"]["content"]

    # Save the summary to a file with a .summary extension.
    base, _ = os.path.splitext(vtt_file)
    summary_filename = base + ".summary.txt"
    with open(summary_filename, 'w', encoding='utf-8') as out:
        out.write(summary)
    print(f"Summary saved as {summary_filename}")

if __name__ == "__main__":
    main()
