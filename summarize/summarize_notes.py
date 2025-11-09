"""
Summarize transcripts into markdown study notes using OpenAI GPT.
"""
import os
from typing import Optional

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


PROMPT_TEMPLATE = """Convert the following transcript into well-structured markdown study notes.

Transcript:
{transcript}

Please format the output as:
- Clear headings and subheadings
- Key points as bullet lists
- Important concepts highlighted
- Summary section at the end

Make the notes concise but comprehensive, focusing on the main topics and key takeaways."""


def check_openai_available() -> bool:
    """Check if OpenAI library is installed and API key is available."""
    if OpenAI is None:
        return False
    
    api_key = os.getenv("OPENAI_API_KEY")
    return api_key is not None and api_key.strip() != ""


def summarize_transcript(
    transcript: str,
    model: str = "gpt-4o-mini",
    temperature: float = 0.3
) -> str:
    """
    Convert transcript into markdown study notes using OpenAI GPT.
    
    Args:
        transcript: Raw transcript text
        model: OpenAI model to use (default: "gpt-4o-mini" for cost efficiency)
        temperature: Sampling temperature (0.0-2.0). Lower = more focused.
        
    Returns:
        Formatted markdown notes
        
    Raises:
        ValueError: If transcript is empty or OpenAI API key not set
        ImportError: If OpenAI library is not installed
        RuntimeError: If summarization fails
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
    
    # Validate transcript
    if not transcript or not transcript.strip():
        raise ValueError("Transcript is empty. Cannot generate notes from empty transcript.")
    
    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Format prompt with transcript
    prompt = PROMPT_TEMPLATE.format(transcript=transcript)
    
    try:
        # Call OpenAI API
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that converts transcripts into well-structured markdown study notes."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=temperature,
            max_tokens=2000  # Adjust based on expected output length
        )
        
        # Extract markdown notes from response
        notes = response.choices[0].message.content.strip()
        
        return notes
        
    except Exception as e:
        error_msg = str(e)
        
        # Handle common errors
        if "rate_limit" in error_msg.lower() or "429" in error_msg:
            raise RuntimeError("OpenAI API rate limit exceeded. Please try again later.")
        elif "invalid_api_key" in error_msg.lower() or "401" in error_msg:
            raise ValueError("Invalid OpenAI API key. Please check your API key.")
        elif "insufficient_quota" in error_msg.lower():
            raise RuntimeError("OpenAI API quota exceeded. Please check your account.")
        elif "context_length" in error_msg.lower() or "token" in error_msg.lower():
            raise ValueError(
                f"Transcript too long for model {model}. "
                f"Consider using a model with larger context window or chunking the transcript."
            )
        else:
            raise RuntimeError(f"Summarization failed: {error_msg}")


if __name__ == "__main__":
    # TODO: Add main execution logic
    pass

