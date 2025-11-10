# Design: Duplicate Prevention and Resume Functionality

## Current State

### Existing Features
- `skip_existing` parameter in `process_channel()` that checks for existing notes
- Checks for files containing video_id in filename: `notes_dir.glob(f"*{video_id}*")`
- Problem: Notes are named `channel_name:title.md`, so video_id might not be in filename

### Limitations
1. **Duplicate Detection**: Only checks filename pattern, not reliable for all naming schemes
2. **No Resume Support**: Always processes from the beginning of the scraped list
3. **No Tracking**: No persistent record of which videos have been processed
4. **No Order Tracking**: Doesn't know which video was processed last

## Proposed Solution

### 1. Processing State Tracker (JSON File)

**Location**: `output/{channel_name}/.processing_state.json`

**Structure**:
```json
{
  "channel_url": "https://www.tiktok.com/@raneshguruparan",
  "channel_name": "raneshguruparan",
  "last_processed_url": "https://www.tiktok.com/@raneshguruparan/video/7570722891772316983",
  "last_processed_index": 5,
  "last_updated": "2025-01-27T12:00:00Z",
  "processed_videos": {
    "7570722891772316983": {
      "url": "https://www.tiktok.com/@raneshguruparan/video/7570722891772316983",
      "video_id": "7570722891772316983",
      "notes_file": "raneshguruparan:Study_Notes_Random_Forest.md",
      "processed_at": "2025-01-27T11:45:00Z",
      "status": "success"
    }
  },
  "total_processed": 5,
  "total_skipped": 0,
  "total_failed": 0
}
```

### 2. Improved Duplicate Detection

**Methods**:
1. **Check tracking file**: Look up video_id in `processed_videos` dict
2. **Check notes file exists**: Verify the notes file path from tracking file still exists
3. **Fallback to filename pattern**: If tracking file missing, use current method

**Benefits**:
- Reliable even if notes are renamed
- Fast lookup (O(1) dict lookup)
- Tracks processing history

### 3. Resume Functionality

**Strategy**:
1. Load processing state from `.processing_state.json`
2. Find `last_processed_url` in the newly scraped video list
3. If found, start processing from the next video after that index
4. If not found (new channel or state lost), process from beginning
5. Update state after each successful processing

**Benefits**:
- Only processes new videos
- Handles interruptions gracefully
- Can resume from exact position

### 4. Implementation Details

#### Functions to Add:

1. **`load_processing_state(channel_dir)`**
   - Load JSON state file if exists
   - Return dict or None

2. **`save_processing_state(channel_dir, state)`**
   - Save state to JSON file
   - Atomic write (write to temp, then rename)

3. **`is_video_processed(video_id, state, notes_dir)`**
   - Check tracking file first
   - Verify notes file exists
   - Fallback to filename pattern

4. **`find_resume_index(video_urls, last_processed_url)`**
   - Find index of last_processed_url in video_urls
   - Return index + 1 (next video) or 0 if not found

5. **`update_processing_state(state, video_id, video_url, notes_file, status)`**
   - Add/update entry in processed_videos
   - Update last_processed_url and index
   - Update totals

### 5. User Experience

**Command Line Options**:
```bash
# Process all videos, skip existing
python3 process_channel.py <channel_url>

# Process all videos, including existing (reprocess)
python3 process_channel.py <channel_url> --reprocess

# Process only new videos (resume from last)
python3 process_channel.py <channel_url> --resume

# Clear state and start fresh
python3 process_channel.py <channel_url> --reset
```

**Default Behavior**:
- `skip_existing=True` (default): Skip videos with existing notes
- `resume=True` (default): Resume from last processed video
- Both can be disabled with flags

### 6. Edge Cases

1. **State file corrupted**: Fallback to filename pattern check
2. **Notes file deleted but in state**: Re-process (state says processed, but file missing)
3. **Video order changed**: Use URL matching, not index (URLs are stable)
4. **Multiple processes**: File locking or atomic writes to prevent conflicts

### 7. Migration Path

- Existing installations: First run creates state file from existing notes
- Backward compatible: Falls back to filename pattern if state missing
- No breaking changes to existing functionality

