#!/usr/bin/env python3
"""
Complete pipeline: Download video → Extract audio → Transcribe → Generate notes
"""
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from download.download_video import download_video, get_video_info
from audio.extract_audio import extract_audio
from transcript.transcribe import transcribe_audio, check_openai_available
from summarize.summarize_notes import summarize_transcript


def run_pipeline(url: str, output_dir: str = "output", channel_name: str = None, video_num: int = None, total_videos: int = None):
    """
    Run complete pipeline from video URL to study notes.
    
    Args:
        url: TikTok or YouTube video URL
        output_dir: Base directory to save all outputs
        channel_name: Optional channel name (if not provided, will be extracted from URL)
        video_num: Optional video number (for progress display)
        total_videos: Optional total videos (for progress display)
    """
    progress_prefix = ""
    if video_num is not None and total_videos is not None:
        progress_prefix = f"[Video {video_num}/{total_videos}] "
    
    print("=" * 70)
    print(f"{progress_prefix}COMPLETE PIPELINE: Video URL → Study Notes")
    print("=" * 70)
    print(f"\nURL: {url}\n")
    
    # Extract video ID and channel name for filename
    import re
    video_id = None
    
    if "tiktok.com" in url:
        # Extract TikTok username if not provided
        if channel_name is None:
            match = re.search(r'@([^/]+)', url)
            channel_name = match.group(1) if match else "tiktok_user"
        match = re.search(r'/video/(\d+)', url)
        video_id = match.group(1) if match else "tiktok_video"
    elif "youtube.com" in url or "youtu.be" in url:
        match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url)
        video_id = match.group(1) if match else "youtube_video"
        # Try to get channel name from video info if not provided
        if channel_name is None:
            try:
                info = get_video_info(url)
                channel_name = info.get('uploader', info.get('channel', 'youtube_channel'))
                # Clean channel name for filename (remove special chars)
                channel_name = re.sub(r'[^\w\s-]', '', channel_name).strip().replace(' ', '_')
            except:
                channel_name = "youtube_channel"
    else:
        video_id = "video"
        if channel_name is None:
            channel_name = "unknown_channel"
    
    # Fallback if channel name not found
    if not channel_name:
        channel_name = "unknown_channel"
    
    # Clean channel name for directory (remove special chars, lowercase)
    channel_name_clean = re.sub(r'[^\w\s-]', '', channel_name).strip().replace(' ', '_').lower()
    
    # Create output directory structure with channel subfolder
    output_path = Path(output_dir) / channel_name_clean
    videos_dir = output_path / "videos"
    audio_dir = output_path / "audio"
    transcripts_dir = output_path / "transcripts"
    notes_dir = output_path / "notes"
    
    # Create all directories
    videos_dir.mkdir(parents=True, exist_ok=True)
    audio_dir.mkdir(parents=True, exist_ok=True)
    transcripts_dir.mkdir(parents=True, exist_ok=True)
    notes_dir.mkdir(parents=True, exist_ok=True)
    
    # Step 1: Download video
    print(f"📹 Step 1/6: Downloading video...")
    try:
        video_path = str(videos_dir / f"{video_id}.mp4")
        downloaded_path = download_video(url, video_path)
        print(f"✅ Video downloaded: {downloaded_path}")
        print(f"   File size: {Path(downloaded_path).stat().st_size / (1024*1024):.2f} MB")
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return None
    
    # Step 2: Extract audio
    print(f"\n🎤 Step 2/6: Extracting audio from video...")
    try:
        audio_path = str(audio_dir / f"{video_id}.wav")
        extracted_audio = extract_audio(downloaded_path, audio_path)
        print(f"✅ Audio extracted: {extracted_audio}")
        print(f"   File size: {Path(extracted_audio).stat().st_size / (1024*1024):.2f} MB")
    except Exception as e:
        print(f"❌ Audio extraction failed: {e}")
        return None
    
    # Step 3: Transcribe audio
    print(f"\n📝 Step 3/6: Transcribing audio to text...")
    from transcript.transcribe import check_whisper_local_available
    
    # Use local Whisper if available, otherwise try API
    use_local = check_whisper_local_available()
    if use_local:
        print("   Using local Whisper model (no API key needed)")
    elif not check_openai_available():
        print("⚠️  Local Whisper not available and OPENAI_API_KEY not set.")
        print("   Install local Whisper: pip install openai-whisper")
        print("   Or set API key: export OPENAI_API_KEY='your-key-here'")
        print("\n✅ Pipeline completed up to audio extraction.")
        print(f"   Audio file: {extracted_audio}")
        return None
    else:
        print("   Using OpenAI Whisper API")
    
    try:
        transcript = transcribe_audio(extracted_audio, language="en", use_local=use_local, model_size="base")
        print(f"✅ Transcript created: {len(transcript)} characters")
        
        # Save transcript
        transcript_path = str(transcripts_dir / f"{video_id}.txt")
        with open(transcript_path, "w", encoding="utf-8") as f:
            f.write(transcript)
        print(f"✅ Transcript saved to: {transcript_path}")
        
        # Show preview
        print("\n--- Transcript Preview (first 500 chars) ---")
        print(transcript[:500] + "..." if len(transcript) > 500 else transcript)
        print("--- End Preview ---\n")
        
    except Exception as e:
        print(f"❌ Transcription failed: {e}")
        return None
    
    # Step 4: Generate notes
    print(f"📚 Step 4/6: Generating markdown notes from transcript...")
    try:
        notes = summarize_transcript(transcript, model="gpt-4o-mini")
        print(f"✅ Notes generated: {len(notes)} characters")
        
        # Generate title from notes using AI
        print(f"\n📝 Step 5/6: Generating title for notes...")
        try:
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            
            # Extract title from notes (first heading) or generate one
            title_match = re.search(r'^#\s+(.+)$', notes, re.MULTILINE)
            if title_match:
                title = title_match.group(1).strip()
            else:
                # Generate a concise title from transcript
                title_response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": "Generate a concise, descriptive title (3-8 words) for study notes based on the transcript. Return only the title, no quotes or extra text."
                        },
                        {
                            "role": "user",
                            "content": f"Transcript: {transcript[:500]}\n\nGenerate a concise title for these study notes:"
                        }
                    ],
                    temperature=0.3,
                    max_tokens=20
                )
                title = title_response.choices[0].message.content.strip().strip('"').strip("'")
            
            # Clean title for filename (remove special chars, limit length)
            title_clean = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '_')
            title_clean = title_clean[:50]  # Limit length
            
            # Create filename: channel_name:title.md
            notes_filename = f"{channel_name}:{title_clean}.md"
            
        except Exception as e:
            print(f"⚠️  Title generation failed, using video ID: {e}")
            notes_filename = f"{channel_name}:{video_id}.md"
        
        # Save notes
        notes_path = str(notes_dir / notes_filename)
        with open(notes_path, "w", encoding="utf-8") as f:
            f.write(notes)
        print(f"✅ Notes saved to: {notes_path}")
        
        # Show notes
        print("\n" + "=" * 70)
        print("GENERATED STUDY NOTES")
        print("=" * 70)
        print(notes)
        print("=" * 70)
        
        # Step 6: Clean up intermediate files
        print(f"\n🧹 Step 6/6: Cleaning up intermediate files...")
        files_deleted = []
        files_to_delete = [
            ("Video", Path(downloaded_path)),
            ("Audio", Path(extracted_audio)),
            ("Transcript", Path(transcript_path))
        ]
        
        for file_type, file_path in files_to_delete:
            if file_path.exists():
                try:
                    file_path.unlink()
                    files_deleted.append(file_type)
                    print(f"✅ Deleted {file_type.lower()}: {file_path.name}")
                except Exception as e:
                    print(f"⚠️  Failed to delete {file_type.lower()}: {e}")
            else:
                print(f"ℹ️  {file_type} file not found (may have been deleted already): {file_path.name}")
        
        if files_deleted:
            print(f"✅ Cleaned up {len(files_deleted)} intermediate file(s)")
        else:
            print("ℹ️  No intermediate files to clean up")
        
        return notes_path
        
    except Exception as e:
        print(f"❌ Note generation failed: {e}")
        return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 run_pipeline.py <video_url> [output_dir]")
        print("\nExample:")
        print("  python3 run_pipeline.py 'https://www.tiktok.com/@preddy_ml/video/7443874677115718942'")
        sys.exit(1)
    
    url = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "output"
    
    run_pipeline(url, output_dir)

