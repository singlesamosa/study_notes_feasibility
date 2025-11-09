"""
Summarize transcripts into markdown study notes.
"""

# TODO: Add necessary imports (openai, etc.)


PROMPT_TEMPLATE = """
Convert the following transcript into well-structured markdown study notes.

Transcript:
{transcript}

Please format the output as:
- Clear headings and subheadings
- Key points as bullet lists
- Important concepts highlighted
- Summary section at the end
"""


def summarize_transcript(transcript: str) -> str:
    """
    Convert transcript into markdown study notes.
    
    Args:
        transcript: Raw transcript text
        
    Returns:
        Formatted markdown notes
    """
    # TODO: Implement summarization logic
    # - Format prompt with transcript
    # - Call LLM API (OpenAI, etc.)
    # - Return formatted markdown
    pass


if __name__ == "__main__":
    # TODO: Add main execution logic
    pass

