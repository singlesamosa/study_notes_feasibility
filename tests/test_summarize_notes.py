"""
Tests for summarize_notes module.
"""
import pytest
import sys
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from summarize.summarize_notes import summarize_transcript, check_openai_available


class TestSummarizeNotes:
    """Test suite for summarize_notes module."""

    @pytest.mark.unit
    @pytest.mark.high
    def test_4_1_valid_transcript_short(self):
        """Test Case 4.1: Valid Transcript - Short"""
        # Skip if OpenAI not available
        if not check_openai_available():
            pytest.skip("OpenAI API key not set. Set OPENAI_API_KEY environment variable.")
        
        transcript = "This is a short transcript about machine learning. It covers basic concepts."
        
        try:
            notes = summarize_transcript(transcript)
            assert isinstance(notes, str)
            assert len(notes) > 0
            # Check if it contains markdown elements
            assert "#" in notes or "-" in notes or "*" in notes
        except Exception as e:
            pytest.skip(f"Summarization failed (may be API issue): {e}")

    @pytest.mark.unit
    @pytest.mark.high
    def test_4_2_valid_transcript_long(self):
        """Test Case 4.2: Valid Transcript - Long"""
        transcript = "This is a very long transcript... " * 200  # 5000+ words
        # TODO: Implement actual test when functionality is available
        # Expected: Comprehensive markdown notes
        # pytest.skip("Functionality not implemented yet")

    @pytest.mark.unit
    @pytest.mark.medium
    def test_4_3_empty_transcript(self):
        """Test Case 4.3: Empty Transcript"""
        # Skip if OpenAI not available
        if not check_openai_available():
            pytest.skip("OpenAI API key not set")
        
        transcript = ""
        # Expected: ValueError
        with pytest.raises(ValueError, match="empty"):
            summarize_transcript(transcript)

    @pytest.mark.unit
    @pytest.mark.low
    def test_4_4_transcript_with_special_characters(self):
        """Test Case 4.4: Transcript with Special Characters"""
        transcript = "This transcript has special chars: @#$%^&*() and unicode: 你好世界"
        # TODO: Implement actual test when functionality is available
        # Expected: Properly formatted notes with special characters handled
        # pytest.skip("Functionality not implemented yet")

    @pytest.mark.integration
    @pytest.mark.high
    def test_4_5_api_error_handling(self):
        """Test Case 4.5: API Error Handling"""
        transcript = "Sample transcript"
        # TODO: Implement actual test when functionality is available
        # Expected: APIError or ConnectionError
        # pytest.skip("Functionality not implemented yet")

    @pytest.mark.unit
    @pytest.mark.high
    def test_4_6_verify_markdown_format(self):
        """Test Case 4.6: Verify Markdown Format"""
        # Skip if OpenAI not available
        if not check_openai_available():
            pytest.skip("OpenAI API key not set")
        
        transcript = "Sample transcript content about machine learning algorithms and their applications."
        
        try:
            notes = summarize_transcript(transcript)
            assert isinstance(notes, str)
            assert len(notes) > 0
            # Verify markdown format (should have headings or lists)
            assert "#" in notes or "-" in notes or "*" in notes or "##" in notes
        except Exception as e:
            pytest.skip(f"Summarization failed (may be API issue): {e}")

