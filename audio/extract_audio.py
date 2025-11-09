"""
Extract audio from video files using FFmpeg.
"""
import subprocess
from pathlib import Path
from typing import Optional


def check_ffmpeg_installed() -> bool:
    """Check if FFmpeg is installed and available."""
    try:
        subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def extract_audio(video_path: str, output_path: Optional[str] = None) -> str:
    """
    Extract audio from a video file and save as WAV.
    
    Args:
        video_path: Path to input video file (.mp4, .avi, etc.)
        output_path: Optional path to output audio file (.wav).
                    If not provided, uses video_path with .wav extension.
        
    Returns:
        Path to extracted audio file
        
    Raises:
        FileNotFoundError: If video file doesn't exist or FFmpeg not installed
        ValueError: If video file has no audio track
        RuntimeError: If FFmpeg extraction fails
    """
    # Check if FFmpeg is installed
    if not check_ffmpeg_installed():
        raise FileNotFoundError(
            "FFmpeg is not installed. Install it from https://ffmpeg.org/"
        )
    
    # Validate input file exists
    video_file = Path(video_path)
    if not video_file.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")
    
    # Determine output path
    if output_path is None:
        output_path = str(video_file.with_suffix('.wav'))
    else:
        output_path = str(Path(output_path))
    
    # Create output directory if it doesn't exist
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # FFmpeg command to extract audio:
    # -i: input file
    # -vn: disable video (no video output)
    # -acodec pcm_s16le: PCM 16-bit little-endian audio codec
    # -ar 16000: sample rate 16000 Hz (optimal for Whisper)
    # -ac 1: mono audio (1 channel)
    # -y: overwrite output file if it exists
    cmd = [
        "ffmpeg",
        "-i", str(video_path),
        "-vn",  # No video
        "-acodec", "pcm_s16le",  # PCM 16-bit
        "-ar", "16000",  # 16kHz sample rate
        "-ac", "1",  # Mono
        "-y",  # Overwrite output
        str(output_path)
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        
        # Verify output file was created
        if not Path(output_path).exists():
            raise RuntimeError(f"Audio file was not created: {output_path}")
        
        # Check file size (should be > 0)
        file_size = Path(output_path).stat().st_size
        if file_size == 0:
            raise ValueError("Extracted audio file is empty - video may have no audio track")
        
        return output_path
        
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr or e.stdout or "Unknown error"
        
        # Check for common errors
        if "does not contain any stream" in error_msg or "No audio stream" in error_msg:
            raise ValueError(f"Video file has no audio track: {video_path}")
        elif "Invalid data found" in error_msg:
            raise ValueError(f"Invalid video format: {video_path}")
        else:
            raise RuntimeError(f"FFmpeg extraction failed: {error_msg}")


if __name__ == "__main__":
    # TODO: Add main execution logic
    pass

