#!/usr/bin/env python3
"""
Process an entire TikTok or YouTube channel and generate notes for all videos.
"""
import sys
import os
from pathlib import Path
from typing import List, Optional

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from scrape.scrape_videos import scrape_videos, is_tiktok_url, is_youtube_url
from run_pipeline import run_pipeline
from utils.processing_state import (
    load_processing_state,
    save_processing_state,
    create_initial_state,
    is_video_processed,
    find_resume_index,
    update_processing_state,
    extract_video_id
)


def process_channel(
    channel_url: str,
    output_dir: str = "output",
    max_videos: int = None,
    skip_existing: bool = True,
    resume: bool = True,
    reset: bool = False
):
    """
    Process all videos from a channel and generate notes.
    
    Args:
        channel_url: TikTok or YouTube channel URL
        output_dir: Base directory to save all outputs
        max_videos: Maximum number of videos to process (None = all)
        skip_existing: Skip videos that already have notes generated
        resume: Resume from last processed video (default: True)
        reset: Reset processing state and start fresh (default: False)
    """
    print("=" * 70)
    print("CHANNEL PROCESSING: Generate Notes for All Videos")
    print("=" * 70)
    print(f"\nChannel URL: {channel_url}\n")
    
    # Determine max videos
    if max_videos is None:
        if is_tiktok_url(channel_url):
            max_videos = "all"  # Get all TikTok videos
        else:
            max_videos = 10  # Default to 10 for YouTube
    
    # Step 1: Scrape video URLs
    print("📹 Step 1: Scraping video URLs from channel...")
    try:
        video_urls = scrape_videos(channel_url, max_videos=max_videos)
        print(f"✅ Found {len(video_urls)} videos")
        
        if len(video_urls) == 0:
            print("❌ No videos found. Exiting.")
            return
        
        print(f"\nFirst 5 video URLs:")
        for i, url in enumerate(video_urls[:5], 1):
            print(f"  {i}. {url}")
        if len(video_urls) > 5:
            print(f"  ... and {len(video_urls) - 5} more")
        print()
        
    except Exception as e:
        print(f"❌ Failed to scrape channel: {e}")
        return
    
    # Extract channel name from URL
    import re
    channel_name = None
    if is_tiktok_url(channel_url):
        match = re.search(r'@([^/?]+)', channel_url)
        channel_name = match.group(1) if match else None
    elif is_youtube_url(channel_url):
        # Try to extract from channel URL pattern
        match = re.search(r'@([^/?]+)', channel_url)
        if match:
            channel_name = match.group(1)
        else:
            # Try /channel/ or /c/ pattern
            match = re.search(r'/(?:channel|c|user)/([^/?]+)', channel_url)
            if match:
                channel_name = match.group(1)
    
    # Clean channel name for directory
    if channel_name:
        channel_name_clean = re.sub(r'[^\w\s-]', '', channel_name).strip().replace(' ', '_').lower()
    else:
        channel_name_clean = "unknown_channel"
    
    # Channel-specific directories
    channel_dir = Path(output_dir) / channel_name_clean
    notes_dir = channel_dir / "notes"
    notes_dir.mkdir(parents=True, exist_ok=True)
    
    # Load or create processing state
    if reset:
        print("🔄 Resetting processing state...")
        state = create_initial_state(channel_url, channel_name_clean)
        save_processing_state(channel_dir, state)
    else:
        state = load_processing_state(channel_dir)
        if state is None:
            state = create_initial_state(channel_url, channel_name_clean)
            save_processing_state(channel_dir, state)
            print("📝 Created new processing state file")
        else:
            print(f"📝 Loaded processing state: {state.get('total_processed', 0)} videos processed")
            if state.get('last_processed_url'):
                print(f"   Last processed: {state['last_processed_url']}")
    
    # Determine starting index (resume functionality)
    start_index = 0
    if resume and state.get('last_processed_url'):
        start_index = find_resume_index(video_urls, state['last_processed_url'])
        if start_index > 0:
            print(f"▶️  Resuming from video {start_index + 1}/{len(video_urls)}")
            print(f"   (Last processed: {state['last_processed_url']})")
        else:
            print("ℹ️  Last processed video not found in current list, starting from beginning")
    
    # Step 2: Process each video
    print("=" * 70)
    print(f"PROCESSING {len(video_urls) - start_index} VIDEOS (starting from index {start_index + 1})")
    print(f"Channel: {channel_name or 'Unknown'}")
    print("=" * 70)
    print()
    
    successful = 0
    failed = 0
    skipped = 0
    
    for i, video_url in enumerate(video_urls[start_index:], start=start_index + 1):
        print(f"\n{'=' * 70}")
        print(f"📹 Video {i}/{len(video_urls)}: {video_url}")
        print("=" * 70)
        
        # Extract video ID
        video_id = extract_video_id(video_url)
        
        # Check if notes already exist (skip if requested)
        if skip_existing and video_id:
            is_processed, notes_filename = is_video_processed(video_id, state, notes_dir)
            if is_processed:
                print(f"⏭️  Skipping (notes already exist: {notes_filename})")
                print(f"   Progress: {i}/{len(video_urls)} videos processed")
                skipped += 1
                # Update state for skipped video
                state = update_processing_state(state, video_id, video_url, notes_filename, status="skipped")
                save_processing_state(channel_dir, state)
                continue
        
        # Run pipeline for this video with channel name
        notes_path = None
        try:
            notes_path = run_pipeline(video_url, output_dir, channel_name=channel_name, video_num=i, total_videos=len(video_urls))
            if notes_path:
                successful += 1
                notes_filename = Path(notes_path).name
                print(f"✅ Video {i}/{len(video_urls)} completed successfully")
                
                # Update state for successful processing
                if video_id:
                    state = update_processing_state(state, video_id, video_url, notes_filename, status="success")
                    state["last_processed_index"] = i - 1  # 0-indexed
                    save_processing_state(channel_dir, state)
            else:
                failed += 1
                print(f"⚠️  Video {i}/{len(video_urls)} completed with warnings")
                
                # Update state for failed processing
                if video_id:
                    state = update_processing_state(state, video_id, video_url, None, status="failed")
                    save_processing_state(channel_dir, state)
        except Exception as e:
            failed += 1
            print(f"❌ Video {i}/{len(video_urls)} failed: {e}")
            
            # Update state for failed processing
            if video_id:
                state = update_processing_state(state, video_id, video_url, None, status="failed")
                save_processing_state(channel_dir, state)
            continue
    
    # Summary
    print("\n" + "=" * 70)
    print("CHANNEL PROCESSING SUMMARY")
    print("=" * 70)
    print(f"Total videos: {len(video_urls)}")
    print(f"✅ Successful: {successful}")
    print(f"⏭️  Skipped: {skipped}")
    print(f"❌ Failed: {failed}")
    print(f"📝 Notes location: {notes_dir}")
    print(f"📁 Channel folder: {Path(output_dir) / channel_name_clean}")
    print("=" * 70)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 process_channel.py <channel_url> [output_dir] [max_videos]")
        print("\nExamples:")
        print("  python3 process_channel.py 'https://www.tiktok.com/@username'")
        print("  python3 process_channel.py 'https://www.youtube.com/@channel' output 20")
        print("\nOptions:")
        print("  channel_url: TikTok or YouTube channel URL")
        print("  output_dir: Base directory (default: output)")
        print("  max_videos: Maximum videos to process (default: all for TikTok, 10 for YouTube)")
        sys.exit(1)
    
    channel_url = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "output"
    max_videos = int(sys.argv[3]) if len(sys.argv) > 3 else None
    
    process_channel(channel_url, output_dir, max_videos)

