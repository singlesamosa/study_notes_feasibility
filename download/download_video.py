"""
Download videos from TikTok and YouTube.
"""
import subprocess
import sys
from pathlib import Path
from typing import Optional
import re


def is_tiktok_url(url: str) -> bool:
    """Check if URL is a TikTok URL."""
    return "tiktok.com" in url.lower()


def is_youtube_url(url: str) -> bool:
    """Check if URL is a YouTube URL."""
    youtube_patterns = [
        r'youtube\.com',
        r'youtu\.be',
        r'youtube\.com/watch',
        r'youtube\.com/shorts'
    ]
    return any(re.search(pattern, url.lower()) for pattern in youtube_patterns)


def validate_url(url: str) -> bool:
    """Validate that URL is from a supported platform."""
    return is_tiktok_url(url) or is_youtube_url(url)


def download_video(url: str, output_path: Optional[str] = None) -> str:
    """
    Download video from TikTok or YouTube URL.
    
    Args:
        url: TikTok or YouTube video URL
        output_path: Optional output path. If not provided, uses video ID as filename.
        
    Returns:
        Path to downloaded video file
        
    Raises:
        ValueError: If URL is not from a supported platform
        FileNotFoundError: If yt-dlp is not installed
        subprocess.CalledProcessError: If download fails
    """
    if not validate_url(url):
        raise ValueError(f"Unsupported URL: {url}. Must be from TikTok or YouTube.")
    
    # Check if yt-dlp is installed (try both yt-dlp and python3 -m yt_dlp)
    yt_dlp_cmd = None
    try:
        subprocess.run(
            ["yt-dlp", "--version"],
            capture_output=True,
            check=True
        )
        yt_dlp_cmd = "yt-dlp"
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            subprocess.run(
                ["python3", "-m", "yt_dlp", "--version"],
                capture_output=True,
                check=True
            )
            yt_dlp_cmd = ["python3", "-m", "yt_dlp"]
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise FileNotFoundError(
                "yt-dlp is not installed. Install it with: pip install yt-dlp"
            )
    
    # Determine output path
    if output_path is None:
        # Extract video ID for filename
        if is_tiktok_url(url):
            # TikTok URL format: https://www.tiktok.com/@username/video/1234567890
            match = re.search(r'/video/(\d+)', url)
            video_id = match.group(1) if match else "tiktok_video"
            output_path = f"downloads/{video_id}.mp4"
        elif is_youtube_url(url):
            # YouTube URL format: https://www.youtube.com/watch?v=VIDEO_ID
            match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url)
            video_id = match.group(1) if match else "youtube_video"
            output_path = f"downloads/{video_id}.mp4"
        else:
            output_path = "downloads/video.mp4"
    
    # Create output directory if it doesn't exist
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Download video using yt-dlp
    # -f: best video format
    # -o: output path
    # --no-playlist: download only single video, not playlist
    if yt_dlp_cmd is None:
        # Re-check if not already determined
        try:
            subprocess.run(["yt-dlp", "--version"], capture_output=True, check=True)
            yt_dlp_cmd = "yt-dlp"
        except:
            try:
                subprocess.run(["python3", "-m", "yt_dlp", "--version"], capture_output=True, check=True)
                yt_dlp_cmd = ["python3", "-m", "yt_dlp"]
            except:
                raise FileNotFoundError("yt-dlp is not installed")
    
    # Use format that doesn't require ffmpeg merging
    # Prefer single file format, fallback to best available
    if isinstance(yt_dlp_cmd, str):
        cmd = [
            yt_dlp_cmd,
            "-f", "best[ext=mp4]/best[height<=720]/best",  # Single file, no merging needed
            "-o", str(output_path),
            "--no-playlist",
            "--no-warnings",  # Suppress warnings
            url
        ]
    else:
        cmd = yt_dlp_cmd + [
            "-f", "best[ext=mp4]/best[height<=720]/best",  # Single file, no merging needed
            "-o", str(output_path),
            "--no-playlist",
            "--no-warnings",  # Suppress warnings
            url
        ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        
        # yt-dlp might add extension, so check if file exists
        downloaded_path = Path(output_path)
        if not downloaded_path.exists():
            # Try with .mp4 extension if not already there
            if not output_path.endswith('.mp4'):
                downloaded_path = Path(output_path + '.mp4')
            # If still not found, look for any file in the directory
            if not downloaded_path.exists():
                files = list(output_dir.glob("*"))
                if files:
                    downloaded_path = files[0]
        
        if not downloaded_path.exists():
            raise FileNotFoundError(f"Downloaded video not found at {output_path}")
        
        return str(downloaded_path)
        
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr or e.stdout or "Unknown error"
        raise RuntimeError(f"Failed to download video: {error_msg}")


def get_video_info(url: str) -> dict:
    """
    Get video information without downloading.
    
    Args:
        url: TikTok or YouTube video URL
        
    Returns:
        Dictionary with video information (title, duration, etc.)
    """
    if not validate_url(url):
        raise ValueError(f"Unsupported URL: {url}. Must be from TikTok or YouTube.")
    
    # Try both yt-dlp and python3 -m yt_dlp
    yt_dlp_cmd = None
    try:
        subprocess.run(["yt-dlp", "--version"], capture_output=True, check=True)
        yt_dlp_cmd = ["yt-dlp"]
    except:
        try:
            subprocess.run(["python3", "-m", "yt_dlp", "--version"], capture_output=True, check=True)
            yt_dlp_cmd = ["python3", "-m", "yt_dlp"]
        except:
            raise FileNotFoundError("yt-dlp is not installed")
    
    try:
        result = subprocess.run(
            yt_dlp_cmd + ["--dump-json", url],
            capture_output=True,
            text=True,
            check=True
        )
        import json
        return json.loads(result.stdout)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        raise RuntimeError(f"Failed to get video info: {e}")


if __name__ == "__main__":
    # Example usage
    if len(sys.argv) < 2:
        print("Usage: python download_video.py <url> [output_path]")
        sys.exit(1)
    
    url = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        video_path = download_video(url, output_path)
        print(f"Video downloaded to: {video_path}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

