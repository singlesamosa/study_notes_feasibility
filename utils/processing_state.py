"""
Processing state management for tracking processed videos and resuming from last position.
"""
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List, Tuple


STATE_FILE = ".processing_state.json"


def load_processing_state(channel_dir: Path) -> Optional[Dict]:
    """
    Load processing state from JSON file.
    
    Args:
        channel_dir: Channel output directory (e.g., output/raneshguruparan/)
        
    Returns:
        State dictionary or None if file doesn't exist
    """
    state_file = channel_dir / STATE_FILE
    if not state_file.exists():
        return None
    
    try:
        with open(state_file, 'r', encoding='utf-8') as f:
            state = json.load(f)
        return state
    except (json.JSONDecodeError, IOError) as e:
        print(f"⚠️  Warning: Failed to load processing state: {e}")
        return None


def save_processing_state(channel_dir: Path, state: Dict) -> bool:
    """
    Save processing state to JSON file (atomic write).
    
    Args:
        channel_dir: Channel output directory
        state: State dictionary to save
        
    Returns:
        True if successful, False otherwise
    """
    state_file = channel_dir / STATE_FILE
    temp_file = channel_dir / f"{STATE_FILE}.tmp"
    
    try:
        # Ensure directory exists
        channel_dir.mkdir(parents=True, exist_ok=True)
        
        # Write to temp file first (atomic write)
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
        
        # Atomic rename
        temp_file.replace(state_file)
        return True
    except IOError as e:
        print(f"⚠️  Warning: Failed to save processing state: {e}")
        if temp_file.exists():
            temp_file.unlink()
        return False


def create_initial_state(channel_url: str, channel_name: str) -> Dict:
    """
    Create initial processing state structure.
    
    Args:
        channel_url: Channel URL
        channel_name: Channel name
        
    Returns:
        Initial state dictionary
    """
    return {
        "channel_url": channel_url,
        "channel_name": channel_name,
        "last_processed_url": None,
        "last_processed_index": -1,
        "last_updated": None,
        "processed_videos": {},
        "total_processed": 0,
        "total_skipped": 0,
        "total_failed": 0
    }


def is_video_processed(
    video_id: str,
    state: Optional[Dict],
    notes_dir: Path
) -> Tuple[bool, Optional[str]]:
    """
    Check if a video has already been processed.
    
    Args:
        video_id: Video ID to check
        state: Processing state dictionary (can be None)
        notes_dir: Directory containing notes files
        
    Returns:
        Tuple of (is_processed, notes_filename or None)
    """
    # Method 1: Check tracking file (most reliable)
    if state and "processed_videos" in state:
        if video_id in state["processed_videos"]:
            video_info = state["processed_videos"][video_id]
            notes_filename = video_info.get("notes_file")
            
            # Verify notes file still exists
            if notes_filename:
                notes_path = notes_dir / notes_filename
                if notes_path.exists():
                    return True, notes_filename
                else:
                    # State says processed but file missing - treat as not processed
                    return False, None
    
    # Method 2: Fallback to filename pattern search
    existing_notes = list(notes_dir.glob(f"*{video_id}*"))
    if existing_notes:
        return True, existing_notes[0].name
    
    return False, None


def find_resume_index(video_urls: List[str], last_processed_url: Optional[str]) -> int:
    """
    Find the index to resume from in the video list.
    
    Args:
        video_urls: List of video URLs
        last_processed_url: Last processed video URL from state
        
    Returns:
        Index to start from (0 if not found or None)
    """
    if not last_processed_url:
        return 0
    
    try:
        last_index = video_urls.index(last_processed_url)
        # Resume from next video after last processed
        return last_index + 1
    except ValueError:
        # Last processed URL not in current list (maybe order changed or new scrape)
        return 0


def update_processing_state(
    state: Dict,
    video_id: str,
    video_url: str,
    notes_file: Optional[str],
    status: str = "success"
) -> Dict:
    """
    Update processing state after processing a video.
    
    Args:
        state: Current state dictionary
        video_id: Video ID
        video_url: Video URL
        notes_file: Notes filename (None if failed)
        status: Processing status ("success", "failed", "skipped")
        
    Returns:
        Updated state dictionary
    """
    # Update processed videos dict
    state["processed_videos"][video_id] = {
        "url": video_url,
        "video_id": video_id,
        "notes_file": notes_file,
        "processed_at": datetime.now().isoformat(),
        "status": status
    }
    
    # Update last processed URL and index
    # Note: index will be updated by caller who knows the position
    state["last_processed_url"] = video_url
    state["last_updated"] = datetime.now().isoformat()
    
    # Update totals
    if status == "success":
        state["total_processed"] = state.get("total_processed", 0) + 1
    elif status == "failed":
        state["total_failed"] = state.get("total_failed", 0) + 1
    elif status == "skipped":
        state["total_skipped"] = state.get("total_skipped", 0) + 1
    
    return state


def extract_video_id(video_url: str) -> Optional[str]:
    """
    Extract video ID from URL.
    
    Args:
        video_url: Video URL
        
    Returns:
        Video ID or None
    """
    import re
    
    if "tiktok.com" in video_url:
        match = re.search(r'/video/(\d+)', video_url)
        return match.group(1) if match else None
    elif "youtube.com" in video_url or "youtu.be" in video_url:
        match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', video_url)
        return match.group(1) if match else None
    return None

