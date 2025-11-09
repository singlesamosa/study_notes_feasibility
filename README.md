# Study Notes Feasibility Project

A project to scrape TikTok videos, extract audio, transcribe, and generate study notes.

## Project Structure

```
.
├── scrape/          # Video scraping module
├── audio/           # Audio extraction module
├── transcript/      # Transcription module
├── summarize/       # Note summarization module
├── tests/           # Test suite
├── test_results/    # Test results and dashboard
└── docs/            # Documentation
```

## Running Tests

### Run All Tests and Update Dashboard

To run all tests and automatically update the dashboard:

```bash
python3 run_tests_and_update_dashboard.py
```

This will:
1. Run all tests using pytest
2. Parse the test results
3. Update the HTML dashboard with current test statuses
4. Display a summary

### Run Specific Test Suites

```bash
# Run all tests
python3 -m pytest tests/ -v

# Run download module tests
python3 -m pytest tests/test_download_video.py -v

# Run scrape module tests
python3 -m pytest tests/test_scrape_videos.py -v

# Run audio extraction tests
python3 -m pytest tests/test_extract_audio.py -v
```

### Test Video Downloading Manually

To test downloading videos with real URLs:

```bash
# Test with example script
python3 test_download_example.py

# Or test directly in Python
python3 -c "
from download.download_video import download_video
video_path = download_video('https://www.youtube.com/watch?v=dQw4w9WgXcQ', 'test.mp4')
print(f'Downloaded to: {video_path}')
"
```

### View Test Dashboard

Open `test_results/test_dashboard.html` in your browser to see:
- Test status (Passed/Failed/Pending)
- Test details (Input/Expected Output)
- Filter and search tests
- Real-time statistics

## Test Status

- **Total Tests:** 33
- **Current Status:** See dashboard for latest results

## Development

### Setup

1. **Install FFmpeg** (required for audio extraction):
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt-get install ffmpeg` (Ubuntu/Debian)
   - See `docs/INSTALLATION.md` for detailed instructions

2. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

3. **Install Playwright browsers** (for TikTok scraping):
```bash
playwright install
```

4. **Run tests:**
```bash
python3 run_tests_and_update_dashboard.py
```

See `docs/INSTALLATION.md` for complete setup instructions.

### Test Structure

Tests are organized by module:
- `test_scrape_videos.py` - Scrape module tests
- `test_extract_audio.py` - Audio extraction tests
- `test_transcribe.py` - Transcription tests
- `test_summarize_notes.py` - Summarization tests
- `test_integration.py` - Integration, performance, and edge case tests

## Status Tracker

See `STATUS_TRACKER.md` for project status and module progress.

## Test Plan

See `tests/TEST_PLAN.md` for comprehensive test cases with inputs and expected outputs.
