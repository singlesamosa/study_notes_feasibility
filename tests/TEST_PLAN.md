# Comprehensive Test Suite Plan

## Test Overview
This document outlines comprehensive test cases with inputs and expected outputs for the study notes feasibility project.

---

## Module 1: Scrape Videos (`scrape/scrape_videos.py`)

### Test Case 1.1: Valid TikTok URL - Single Video
**Input:**
```python
url = "https://www.tiktok.com/@username/video/1234567890"
```

**Expected Output:**
```python
[
    "https://www.tiktok.com/@username/video/1234567890"
]
```

**Test Type:** Unit Test  
**Priority:** High

---

### Test Case 1.2: Valid TikTok URL - User Profile Page
**Input:**
```python
url = "https://www.tiktok.com/@username"
```

**Expected Output:**
```python
[
    "https://www.tiktok.com/@username/video/1234567890",
    "https://www.tiktok.com/@username/video/0987654321",
    # ... more video URLs
]
```

**Test Type:** Integration Test  
**Priority:** High

---

### Test Case 1.3: Invalid URL
**Input:**
```python
url = "https://www.youtube.com/watch?v=abc123"
```

**Expected Output:**
```python
[]  # Empty list or raise ValueError
```

**Test Type:** Unit Test  
**Priority:** Medium

---

### Test Case 1.4: Malformed URL
**Input:**
```python
url = "not-a-url"
```

**Expected Output:**
```python
# Raise ValueError or URLError
```

**Test Type:** Unit Test  
**Priority:** Medium

---

### Test Case 1.5: Network Error Handling
**Input:**
```python
url = "https://www.tiktok.com/@username"  # Simulate network failure
```

**Expected Output:**
```python
# Raise ConnectionError or TimeoutError with appropriate message
```

**Test Type:** Integration Test  
**Priority:** Medium

---

## Module 2: Extract Audio (`audio/extract_audio.py`)

### Test Case 2.1: Valid MP4 Video File
**Input:**
```python
video_path = "test_data/sample_video.mp4"
output_path = "test_data/output_audio.wav"
```

**Expected Output:**
```python
"test_data/output_audio.wav"  # File path string
# File should exist and be valid WAV format
```

**Test Type:** Unit Test  
**Priority:** High

---

### Test Case 2.2: Non-existent Video File
**Input:**
```python
video_path = "test_data/nonexistent.mp4"
output_path = "test_data/output_audio.wav"
```

**Expected Output:**
```python
# Raise FileNotFoundError
```

**Test Type:** Unit Test  
**Priority:** High

---

### Test Case 2.3: Invalid Video Format
**Input:**
```python
video_path = "test_data/image.jpg"
output_path = "test_data/output_audio.wav"
```

**Expected Output:**
```python
# Raise ValueError or FFmpeg error indicating invalid format
```

**Test Type:** Unit Test  
**Priority:** Medium

---

### Test Case 2.4: Video Without Audio Track
**Input:**
```python
video_path = "test_data/video_no_audio.mp4"
output_path = "test_data/output_audio.wav"
```

**Expected Output:**
```python
# Raise ValueError or return empty file with appropriate warning
```

**Test Type:** Unit Test  
**Priority:** Medium

---

### Test Case 2.5: Output Directory Doesn't Exist
**Input:**
```python
video_path = "test_data/sample_video.mp4"
output_path = "nonexistent_dir/output_audio.wav"
```

**Expected Output:**
```python
# Either create directory or raise FileNotFoundError
```

**Test Type:** Unit Test  
**Priority:** Low

---

### Test Case 2.6: Verify WAV Format Specifications
**Input:**
```python
video_path = "test_data/sample_video.mp4"
output_path = "test_data/output_audio.wav"
```

**Expected Output:**
```python
# WAV file should have:
# - Sample rate: 16000 Hz
# - Channels: 1 (mono)
# - Codec: PCM 16-bit
```

**Test Type:** Unit Test  
**Priority:** High

---

## Module 3: Transcribe Audio (`transcript/transcribe.py`)

### Test Case 3.1: Valid WAV Audio File - English
**Input:**
```python
audio_path = "test_data/sample_audio.wav"
```

**Expected Output:**
```python
"This is a sample transcript of the audio content. It should contain the full text spoken in the video."
```

**Test Type:** Unit Test  
**Priority:** High

---

### Test Case 3.2: Valid WAV Audio File - Non-English
**Input:**
```python
audio_path = "test_data/spanish_audio.wav"
```

**Expected Output:**
```python
"Este es un ejemplo de transcripción en español."
# Or specify language parameter
```

**Test Type:** Unit Test  
**Priority:** Medium

---

### Test Case 3.3: Non-existent Audio File
**Input:**
```python
audio_path = "test_data/nonexistent.wav"
```

**Expected Output:**
```python
# Raise FileNotFoundError
```

**Test Type:** Unit Test  
**Priority:** High

---

### Test Case 3.4: Invalid Audio Format
**Input:**
```python
audio_path = "test_data/image.jpg"
```

**Expected Output:**
```python
# Raise ValueError indicating invalid audio format
```

**Test Type:** Unit Test  
**Priority:** Medium

---

### Test Case 3.5: Empty/Silent Audio File
**Input:**
```python
audio_path = "test_data/silent_audio.wav"
```

**Expected Output:**
```python
""  # Empty string or appropriate message
```

**Test Type:** Unit Test  
**Priority:** Low

---

### Test Case 3.6: Very Long Audio File (>25 minutes)
**Input:**
```python
audio_path = "test_data/long_audio_30min.wav"
```

**Expected Output:**
```python
# Should handle chunking or raise appropriate error if API limit exceeded
```

**Test Type:** Integration Test  
**Priority:** Medium

---

### Test Case 3.7: API Error Handling
**Input:**
```python
audio_path = "test_data/sample_audio.wav"  # Simulate API failure
```

**Expected Output:**
```python
# Raise APIError or ConnectionError with appropriate message
```

**Test Type:** Integration Test  
**Priority:** High

---

## Module 4: Summarize Notes (`summarize/summarize_notes.py`)

### Test Case 4.1: Valid Transcript - Short
**Input:**
```python
transcript = "This is a short transcript about machine learning. It covers basic concepts."
```

**Expected Output:**
```python
"""# Machine Learning Notes

## Key Concepts
- Basic machine learning concepts

## Summary
This transcript covers fundamental machine learning topics.
"""
```

**Test Type:** Unit Test  
**Priority:** High

---

### Test Case 4.2: Valid Transcript - Long
**Input:**
```python
transcript = "This is a very long transcript..."  # 5000+ words
```

**Expected Output:**
```python
"""# Study Notes

## Main Topics
- Topic 1
- Topic 2
...

## Key Points
- Point 1
- Point 2
...

## Summary
Comprehensive summary of the content.
"""
```

**Test Type:** Unit Test  
**Priority:** High

---

### Test Case 4.3: Empty Transcript
**Input:**
```python
transcript = ""
```

**Expected Output:**
```python
# Either return empty markdown or raise ValueError
```

**Test Type:** Unit Test  
**Priority:** Medium

---

### Test Case 4.4: Transcript with Special Characters
**Input:**
```python
transcript = "This transcript has special chars: @#$%^&*() and unicode: 你好世界"
```

**Expected Output:**
```python
"""# Study Notes

## Content
Properly formatted notes with special characters handled correctly.
"""
```

**Test Type:** Unit Test  
**Priority:** Low

---

### Test Case 4.5: API Error Handling
**Input:**
```python
transcript = "Sample transcript"  # Simulate API failure
```

**Expected Output:**
```python
# Raise APIError or ConnectionError with appropriate message
```

**Test Type:** Integration Test  
**Priority:** High

---

### Test Case 4.6: Verify Markdown Format
**Input:**
```python
transcript = "Sample transcript content"
```

**Expected Output:**
```python
# Should return valid markdown with:
# - Proper headings (#, ##)
# - Bullet lists (-)
# - Code blocks if needed (```)
# - No formatting errors
```

**Test Type:** Unit Test  
**Priority:** High

---

## Integration Tests: Full Pipeline

### Test Case 5.1: Complete Workflow - Single Video
**Input:**
```python
tiktok_url = "https://www.tiktok.com/@username/video/1234567890"
```

**Expected Output:**
```python
# 1. Video downloaded to: test_data/video_1234567890.mp4
# 2. Audio extracted to: test_data/audio_1234567890.wav
# 3. Transcript saved to: test_data/transcript_1234567890.txt
# 4. Notes saved to: test_data/notes_1234567890.md
```

**Test Type:** Integration Test  
**Priority:** High

---

### Test Case 5.2: Complete Workflow - Multiple Videos
**Input:**
```python
tiktok_url = "https://www.tiktok.com/@username"  # Profile with 5 videos
```

**Expected Output:**
```python
# Process all 5 videos:
# - 5 video files
# - 5 audio files
# - 5 transcript files
# - 5 notes files
# - Summary report in test_results/
```

**Test Type:** Integration Test  
**Priority:** High

---

### Test Case 5.3: Pipeline Error Handling - Video Download Fails
**Input:**
```python
tiktok_url = "https://www.tiktok.com/@invalid/video/999"  # Fails to download
```

**Expected Output:**
```python
# Should handle error gracefully:
# - Log error to test_results/error_log.txt
# - Continue with next video if applicable
# - Return appropriate error status
```

**Test Type:** Integration Test  
**Priority:** Medium

---

### Test Case 5.4: Pipeline Error Handling - Transcription Fails
**Input:**
```python
tiktok_url = "https://www.tiktok.com/@username/video/1234567890"
# Audio extraction succeeds, but transcription fails
```

**Expected Output:**
```python
# Should:
# - Keep extracted audio file
# - Log transcription error
# - Skip summarization step
# - Report partial success
```

**Test Type:** Integration Test  
**Priority:** Medium

---

## Performance Tests

### Test Case 6.1: Processing Time - Single Video
**Input:**
```python
tiktok_url = "https://www.tiktok.com/@username/video/1234567890"
# Video duration: 60 seconds
```

**Expected Output:**
```python
# Processing time should be:
# - Video download: < 30 seconds
# - Audio extraction: < 5 seconds
# - Transcription: < 60 seconds
# - Summarization: < 30 seconds
# Total: < 2 minutes
```

**Test Type:** Performance Test  
**Priority:** Medium

---

### Test Case 6.2: Memory Usage
**Input:**
```python
tiktok_url = "https://www.tiktok.com/@username/video/1234567890"
```

**Expected Output:**
```python
# Memory usage should be reasonable:
# - Peak memory: < 500 MB
# - No memory leaks
```

**Test Type:** Performance Test  
**Priority:** Low

---

## Edge Cases

### Test Case 7.1: Very Short Video (< 5 seconds)
**Input:**
```python
tiktok_url = "https://www.tiktok.com/@username/video/1234567890"  # 3 second video
```

**Expected Output:**
```python
# Should handle gracefully:
# - Extract audio successfully
# - Generate transcript (may be short)
# - Generate notes (may be minimal)
```

**Test Type:** Edge Case Test  
**Priority:** Low

---

### Test Case 7.2: Video with Background Music Only
**Input:**
```python
tiktok_url = "https://www.tiktok.com/@username/video/1234567890"  # No speech
```

**Expected Output:**
```python
# Should:
# - Extract audio successfully
# - Return empty or minimal transcript
# - Handle gracefully in notes generation
```

**Test Type:** Edge Case Test  
**Priority:** Low

---

### Test Case 7.3: Video with Multiple Languages
**Input:**
```python
tiktok_url = "https://www.tiktok.com/@username/video/1234567890"  # English + Spanish
```

**Expected Output:**
```python
# Should:
# - Detect multiple languages or use specified language
# - Generate transcript with both languages
# - Format notes appropriately
```

**Test Type:** Edge Case Test  
**Priority:** Low

---

## Test Data Requirements

### Required Test Files:
1. `test_data/sample_video.mp4` - Standard test video (60 seconds, English speech)
2. `test_data/video_no_audio.mp4` - Video without audio track
3. `test_data/silent_audio.wav` - Silent audio file
4. `test_data/long_audio_30min.wav` - Long audio file (>25 minutes)
5. `test_data/spanish_audio.wav` - Spanish language audio
6. `test_data/sample_audio.wav` - Standard test audio

### Test Environment:
- Python 3.8+
- FFmpeg installed
- Playwright browsers installed
- API keys configured (Whisper, OpenAI)
- Network connectivity for integration tests

---

## Test Execution Plan

1. **Unit Tests**: Run individual module tests
2. **Integration Tests**: Run full pipeline tests
3. **Performance Tests**: Measure processing times
4. **Edge Case Tests**: Verify error handling

## Success Criteria

- All unit tests pass
- Integration tests complete successfully
- Error handling works as expected
- Performance meets requirements
- Output files are correctly formatted

