# Audio to Notes Pipeline - Complete Explanation

## Overview

The pipeline converts video audio into structured markdown study notes through three main steps:

```
Video (.mp4) → Audio (.wav) → Transcript (text) → Notes (.md)
```

---

## Step 1: Video → Audio Extraction

**Module:** `audio/extract_audio.py`  
**Tool:** FFmpeg  
**Function:** `extract_audio(video_path, output_path)`

### What Happens:

1. **Input:** Video file (`.mp4`, `.avi`, etc.)
2. **Process:** FFmpeg extracts audio track from video
3. **Output:** Audio file (`.wav`)

### Technical Details:

- **Format:** WAV (uncompressed, high quality)
- **Sample Rate:** 16,000 Hz (optimal for Whisper API)
- **Channels:** Mono (1 channel - reduces file size)
- **Bit Depth:** 16-bit PCM (high quality)

### Why These Settings?

- **16kHz sample rate:** Whisper API works best with 16kHz audio
- **Mono:** Speech doesn't need stereo, reduces file size
- **PCM 16-bit:** High quality, compatible with Whisper

### Code Example:

```python
from audio.extract_audio import extract_audio

# Extract audio from video
audio_path = extract_audio("video.mp4", "audio.wav")
# Result: audio.wav (16kHz, mono, PCM 16-bit)
```

### FFmpeg Command Used:

```bash
ffmpeg -i video.mp4 \
       -vn \                    # No video output
       -acodec pcm_s16le \      # PCM 16-bit little-endian
       -ar 16000 \              # 16kHz sample rate
       -ac 1 \                  # Mono (1 channel)
       -y \                     # Overwrite output
       audio.wav
```

---

## Step 2: Audio → Text Transcription

**Module:** `transcript/transcribe.py`  
**Tool:** OpenAI Whisper API  
**Function:** `transcribe_audio(audio_path, language=None)`

### What Happens:

1. **Input:** Audio file (`.wav`)
2. **Process:** OpenAI Whisper API converts speech to text
3. **Output:** Plain text transcript

### Technical Details:

- **Model:** `whisper-1` (OpenAI's Whisper model)
- **Language:** Auto-detected (or specify with `language="en"`)
- **File Size Limit:** 25 MB maximum
- **Supported Formats:** WAV, MP3, M4A, etc.

### How It Works:

1. Validates audio file exists and is < 25MB
2. Opens audio file in binary mode
3. Sends to OpenAI Whisper API
4. Whisper processes audio and returns text
5. Returns cleaned transcript (stripped whitespace)

### Code Example:

```python
from transcript.transcribe import transcribe_audio

# Transcribe audio to text
transcript = transcribe_audio("audio.wav", language="en")
# Result: "This is the transcribed text from the audio..."
```

### API Call:

```python
client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file_obj,
    language="en",  # Optional, auto-detects if None
    response_format="text"  # Get plain text (not JSON)
)
```

---

## Step 3: Text → Markdown Notes

**Module:** `summarize/summarize_notes.py`  
**Tool:** OpenAI GPT (gpt-4o-mini)  
**Function:** `summarize_transcript(transcript, model="gpt-4o-mini", temperature=0.3)`

### What Happens:

1. **Input:** Raw transcript text
2. **Process:** GPT-4o-mini summarizes and structures the text
3. **Output:** Formatted markdown study notes

### Technical Details:

- **Model:** `gpt-4o-mini` (cost-efficient, fast)
- **Temperature:** 0.3 (lower = more focused, less creative)
- **Max Tokens:** 2000 (adjustable based on expected output length)
- **Format:** Markdown with headings, bullets, summaries

### How It Works:

1. Validates transcript is not empty
2. Formats transcript with prompt template
3. Sends to GPT with system message and user prompt
4. GPT generates structured markdown notes
5. Returns formatted notes

### Prompt Template:

```
Convert the following transcript into well-structured markdown study notes.

Transcript:
{transcript}

Please format the output as:
- Clear headings and subheadings
- Key points as bullet lists
- Important concepts highlighted
- Summary section at the end

Make the notes concise but comprehensive, focusing on the main topics and key takeaways.
```

### Code Example:

```python
from summarize.summarize_notes import summarize_transcript

# Convert transcript to markdown notes
notes = summarize_transcript(transcript, model="gpt-4o-mini")
# Result: "# Study Notes\n\n## Main Topics\n\n- Key point 1\n- Key point 2\n..."
```

### API Call:

```python
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant that converts transcripts into well-structured markdown study notes."
        },
        {
            "role": "user",
            "content": formatted_prompt
        }
    ],
    temperature=0.3,
    max_tokens=2000
)
```

---

## Complete Pipeline Example

Here's how you would use all three steps together:

```python
from audio.extract_audio import extract_audio
from transcript.transcribe import transcribe_audio
from summarize.summarize_notes import summarize_transcript

# Step 1: Extract audio from video
video_path = "video.mp4"
audio_path = extract_audio(video_path, "audio.wav")
print(f"✅ Audio extracted: {audio_path}")

# Step 2: Transcribe audio to text
transcript = transcribe_audio(audio_path, language="en")
print(f"✅ Transcript created ({len(transcript)} characters)")

# Step 3: Convert transcript to markdown notes
notes = summarize_transcript(transcript)
print(f"✅ Notes generated ({len(notes)} characters)")

# Save notes to file
with open("notes.md", "w") as f:
    f.write(notes)
print("✅ Notes saved to notes.md")
```

---

## Output Example

### Input Audio:
A 5-minute video about machine learning basics

### Transcript (Step 2 Output):
```
Machine learning is a subset of artificial intelligence that enables computers to learn from data without being explicitly programmed. There are three main types of machine learning: supervised learning, unsupervised learning, and reinforcement learning. Supervised learning uses labeled data to train models...
```

### Markdown Notes (Step 3 Output):
```markdown
# Machine Learning Basics - Study Notes

## Overview
Machine learning is a subset of artificial intelligence that enables computers to learn from data without explicit programming.

## Main Types of Machine Learning

### 1. Supervised Learning
- Uses labeled data to train models
- Examples: classification, regression
- Common algorithms: linear regression, decision trees

### 2. Unsupervised Learning
- Works with unlabeled data
- Examples: clustering, dimensionality reduction
- Common algorithms: k-means, PCA

### 3. Reinforcement Learning
- Learning through trial and error
- Uses rewards and penalties
- Common applications: game playing, robotics

## Key Takeaways
- Machine learning enables computers to learn from data
- Three main types: supervised, unsupervised, reinforcement
- Each type has different use cases and algorithms

## Summary
Machine learning is a powerful subset of AI that allows computers to learn patterns from data. The three main types each serve different purposes and use different approaches to learning.
```

---

## Error Handling

Each step includes comprehensive error handling:

### Step 1 (Audio Extraction):
- ✅ Checks FFmpeg is installed
- ✅ Validates video file exists
- ✅ Handles missing audio tracks
- ✅ Handles invalid video formats

### Step 2 (Transcription):
- ✅ Checks OpenAI library installed
- ✅ Validates API key is set
- ✅ Checks file size (< 25MB)
- ✅ Handles rate limits and quota errors
- ✅ Handles invalid API keys

### Step 3 (Summarization):
- ✅ Checks OpenAI library installed
- ✅ Validates API key is set
- ✅ Validates transcript is not empty
- ✅ Handles rate limits and quota errors
- ✅ Handles context length errors (transcript too long)

---

## Performance Considerations

### File Sizes:
- **Video:** Typically 1-100 MB
- **Audio (WAV):** ~1-10 MB (depends on video length)
- **Transcript:** ~1-50 KB (text is small)
- **Notes:** ~2-20 KB (summarized)

### Processing Time:
- **Audio Extraction:** 1-10 seconds (depends on video length)
- **Transcription:** 5-30 seconds (depends on audio length, API response time)
- **Summarization:** 2-10 seconds (depends on transcript length, API response time)

### API Costs (OpenAI):
- **Whisper API:** ~$0.006 per minute of audio
- **GPT-4o-mini:** ~$0.15 per 1M input tokens, ~$0.60 per 1M output tokens

---

## Dependencies

### Required:
- **FFmpeg:** For audio extraction
- **OpenAI Python Library:** For transcription and summarization
- **OpenAI API Key:** Set as environment variable `OPENAI_API_KEY`

### Optional:
- **Playwright:** For TikTok scraping (not needed for audio→notes pipeline)
- **yt-dlp:** For video downloading (not needed for audio→notes pipeline)

---

## Next Steps

The pipeline is ready for integration into a main script that:
1. Downloads videos from URLs
2. Extracts audio
3. Transcribes audio
4. Generates notes
5. Saves everything to organized folders


