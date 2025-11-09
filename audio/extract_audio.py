"""
Extract audio from video files using FFmpeg.
"""

import subprocess
# TODO: Add necessary imports


def extract_audio(video_path: str, output_path: str) -> str:
    """
    Extract audio from a video file and save as WAV.
    
    Args:
        video_path: Path to input video file (.mp4)
        output_path: Path to output audio file (.wav)
        
    Returns:
        Path to extracted audio file
    """
    # TODO: Implement FFmpeg command
    # Example: ffmpeg -i input.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 output.wav
    # subprocess.run([...])
    pass


if __name__ == "__main__":
    # TODO: Add main execution logic
    pass

