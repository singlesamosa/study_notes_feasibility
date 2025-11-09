"""
Transcribe audio files using OpenAI Whisper (local or API).
"""
import os
from pathlib import Path
from typing import Optional

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()  # Load .env file if present
except ImportError:
    pass  # python-dotenv not installed, use system env vars only

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

try:
    import whisper
    WHISPER_LOCAL_AVAILABLE = True
except ImportError:
    WHISPER_LOCAL_AVAILABLE = False
    whisper = None


def check_openai_available() -> bool:
    """Check if OpenAI library is installed and API key is available."""
    if OpenAI is None:
        return False
    
    api_key = os.getenv("OPENAI_API_KEY")
    return api_key is not None and api_key.strip() != ""


def check_whisper_local_available() -> bool:
    """Check if local Whisper is installed and available."""
    return WHISPER_LOCAL_AVAILABLE


def transcribe_audio(
    audio_path: str,
    language: Optional[str] = None,
    use_local: bool = True,
    model_size: str = "base"
) -> str:
    """
    Transcribe audio file to text using OpenAI Whisper (local or API).
    
    Args:
        audio_path: Path to audio file (.wav, .mp3, etc.)
        language: Optional language code (e.g., 'en', 'es'). 
                 If None, Whisper will auto-detect.
        use_local: If True, use local Whisper model. If False, use OpenAI API.
                  Default: True (use local if available)
        model_size: Whisper model size for local transcription.
                   Options: "tiny", "base", "small", "medium", "large"
                   Default: "base" (good balance of speed and accuracy)
        
    Returns:
        Transcribed text
        
    Raises:
        FileNotFoundError: If audio file doesn't exist
        ImportError: If required libraries are not installed
        ValueError: If OpenAI API key is not set (when using API)
        RuntimeError: If transcription fails
    """
    # Validate input file exists
    audio_file = Path(audio_path)
    if not audio_file.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    # Try local Whisper first if requested
    if use_local and check_whisper_local_available():
        return _transcribe_local(audio_path, language, model_size)
    
    # Fall back to API if local not available or not requested
    if not use_local or not check_whisper_local_available():
        return _transcribe_api(audio_path, language)
    
    # Should not reach here, but just in case
    raise RuntimeError("No transcription method available. Install openai-whisper or set OPENAI_API_KEY.")


def _transcribe_local(audio_path: str, language: Optional[str], model_size: str) -> str:
    """Transcribe using local Whisper model."""
    if not check_whisper_local_available():
        raise ImportError(
            "Local Whisper is not installed. Install it with: pip install openai-whisper"
        )
    
    try:
        # Load Whisper model (will download on first use)
        print(f"Loading Whisper model '{model_size}' (this may take a moment on first run)...")
        model = whisper.load_model(model_size)
        
        # Transcribe audio
        print(f"Transcribing audio: {audio_path}")
        result = model.transcribe(
            audio_path,
            language=language,  # None means auto-detect
            verbose=False  # Set to True for progress output
        )
        
        # Extract text from result
        transcript = result["text"].strip()
        return transcript
        
    except Exception as e:
        raise RuntimeError(f"Local transcription failed: {e}")


def _transcribe_api(audio_path: str, language: Optional[str]) -> str:
    """Transcribe using OpenAI Whisper API."""
    # Check if OpenAI is available
    if OpenAI is None:
        raise ImportError(
            "OpenAI library is not installed. Install it with: pip install openai"
        )
    
    if not check_openai_available():
        raise ValueError(
            "OpenAI API key is not set. Set it with: export OPENAI_API_KEY='your-key'"
        )
    
    # Check file size (Whisper API has a 25MB limit)
    audio_file = Path(audio_path)
    file_size = audio_file.stat().st_size
    max_size = 25 * 1024 * 1024  # 25 MB
    
    if file_size > max_size:
        raise ValueError(
            f"Audio file too large: {file_size / (1024*1024):.2f} MB. "
            f"Whisper API limit is 25 MB. Consider chunking the audio or using local Whisper."
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
            raise RuntimeError(f"API transcription failed: {error_msg}")


if __name__ == "__main__":
    # TODO: Add main execution logic
    pass

