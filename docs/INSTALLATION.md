# Installation Guide

## Prerequisites

### 1. Python 3.8+
```bash
python3 --version
```

### 2. FFmpeg (Required for Audio Extraction)

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**Linux (Fedora):**
```bash
sudo dnf install ffmpeg
```

**Windows:**
1. Download from https://ffmpeg.org/download.html
2. Extract and add to PATH
3. Or use: `choco install ffmpeg` (if Chocolatey is installed)

**Verify installation:**
```bash
ffmpeg -version
```

### 3. Python Dependencies

```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install pytest pytest-cov playwright openai yt-dlp
```

### 4. Playwright Browsers (for TikTok scraping)

```bash
playwright install
```

Or install only Chromium:
```bash
playwright install chromium
```

## Setup Steps

1. **Clone the repository:**
```bash
git clone https://github.com/singlesamosa/study_notes_feasibility.git
cd study_notes_feasibility
```

2. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

3. **Install FFmpeg** (see above)

4. **Install Playwright browsers:**
```bash
playwright install
```

5. **Verify installation:**
```bash
python3 -m pytest tests/ -v
```

## Optional: API Keys

For transcription and summarization, you'll need:

1. **OpenAI API Key** (for Whisper transcription and GPT summarization)
   - Get from: https://platform.openai.com/api-keys
   - Set environment variable: `export OPENAI_API_KEY="your-key-here"`

## Troubleshooting

### FFmpeg not found
- Make sure FFmpeg is installed and in your PATH
- Try: `which ffmpeg` to check if it's accessible
- On macOS, ensure Homebrew is up to date: `brew update`

### Playwright browsers not installed
- Run: `playwright install`
- Or install specific browser: `playwright install chromium`

### yt-dlp issues
- Update yt-dlp: `pip install --upgrade yt-dlp`
- Check if it's accessible: `python3 -m yt_dlp --version`


