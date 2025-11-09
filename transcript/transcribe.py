"""
Transcribe audio files using OpenAI Whisper API.
"""
import os
from pathlib import Path
from typing import Optional

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


def check_openai_available() -> bool:
    """Check if OpenAI library is installed and API key is available."""
    if OpenAI is None:
        return False
    
    api_key = os.getenv("OPENAI_API_KEY")
    return api_key is not None and api_key.strip() != ""


def transcribe_audio(audio_path: str, language: Optional[str] = None) -> str:
    """
    Transcribe audio file to text using OpenAI Whisper API.
    
    Args:
        audio_path: Path to audio file (.wav, .mp3, etc.)
        language: Optional language code (e.g., 'en', 'es'). 
                 If None, Whisper will auto-detect.
        
    Returns:
        Transcribed text
        
    Raises:
        FileNotFoundError: If audio file doesn't exist
        ImportError: If OpenAI library is not installed
        ValueError: If OpenAI API key is not set
        RuntimeError: If transcription fails
    """
    # Check if OpenAI is available
    if OpenAI is None:
        raise ImportError(
            "OpenAI library is not installed. Install it with: pip install openai"
        )
    
    if not check_openai_available():
        raise ValueError(
            "OpenAI API key is not set. Set it with: export OPENAI_API_KEY='your-key'"
        )
    
    # Validate input file exists
    audio_file = Path(audio_path)
    if not audio_file.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    # Check file size (Whisper API has a 25MB limit)
    file_size = audio_file.stat().st_size
    max_size = 25 * 1024 * 1024  # 25 MB
    
    if file_size > max_size:
        raise ValueError(
            f"Audio file too large: {file_size / (1024*1024):.2f} MB. "
            f"Whisper API limit is 25 MB. Consider chunking the audio."
        )
    
    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    try:
        # Open audio file and transcribe
        with open(audio_path, "rb") as audio_file_obj:
            # Call Whisper API
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file_obj,
                language=language,  # None means auto-detect
                response_format="text"  # Get plain text
            )
        
        # If response is a string, return it directly
        if isinstance(transcript, str):
            return transcript.strip()
        
        # Otherwise, extract text from response object
        return str(transcript).strip()
        
    except Exception as e:
        error_msg = str(e)
        
        # Handle common errors
        if "rate_limit" in error_msg.lower() or "429" in error_msg:
            raise RuntimeError("OpenAI API rate limit exceeded. Please try again later.")
        elif "invalid_api_key" in error_msg.lower() or "401" in error_msg:
            raise ValueError("Invalid OpenAI API key. Please check your API key.")
        elif "insufficient_quota" in error_msg.lower():
            raise RuntimeError("OpenAI API quota exceeded. Please check your account.")
        else:
            raise RuntimeError(f"Transcription failed: {error_msg}")


if __name__ == "__main__":
    # TODO: Add main execution logic
    pass

