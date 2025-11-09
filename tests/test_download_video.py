"""
Tests for download_video module.
"""
import pytest
import sys
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from download.download_video import (
    download_video,
    is_tiktok_url,
    is_youtube_url,
    validate_url,
    get_video_info
)


class TestDownloadVideo:
    """Test suite for download_video module."""

    @pytest.mark.unit
    @pytest.mark.high
    def test_is_tiktok_url_valid(self):
        """Test TikTok URL detection."""
        assert is_tiktok_url("https://www.tiktok.com/@user/video/123")
        assert is_tiktok_url("https://tiktok.com/@user/video/123")
        assert not is_tiktok_url("https://www.youtube.com/watch?v=123")

    @pytest.mark.unit
    @pytest.mark.high
    def test_is_youtube_url_valid(self):
        """Test YouTube URL detection."""
        assert is_youtube_url("https://www.youtube.com/watch?v=123")
        assert is_youtube_url("https://youtu.be/123")
        assert is_youtube_url("https://www.youtube.com/shorts/123")
        assert not is_youtube_url("https://www.tiktok.com/@user/video/123")

    @pytest.mark.unit
    @pytest.mark.high
    def test_validate_url_supported_platforms(self):
        """Test URL validation for supported platforms."""
        assert validate_url("https://www.tiktok.com/@user/video/123")
        assert validate_url("https://www.youtube.com/watch?v=123")
        assert not validate_url("https://www.vimeo.com/video/123")

    @pytest.mark.integration
    @pytest.mark.high
    def test_download_tiktok_video(self):
        """Test downloading a TikTok video."""
        # Use a known public TikTok video URL for testing
        url = "https://www.tiktok.com/@tiktok/video/1234567890"  # Replace with real URL
        # TODO: Implement actual test when functionality is available
        # output_path = "test_data/tiktok_video.mp4"
        # video_path = download_video(url, output_path)
        # assert Path(video_path).exists()
        # pytest.skip("Requires real TikTok URL and yt-dlp installation")

    @pytest.mark.integration
    @pytest.mark.high
    def test_download_youtube_video(self):
        """Test downloading a YouTube video."""
        # Use a known public YouTube video URL for testing
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Roll - always available
        # TODO: Implement actual test when functionality is available
        # output_path = "test_data/youtube_video.mp4"
        # video_path = download_video(url, output_path)
        # assert Path(video_path).exists()
        # pytest.skip("Requires yt-dlp installation")

    @pytest.mark.unit
    @pytest.mark.medium
    def test_download_unsupported_url(self):
        """Test downloading from unsupported platform."""
        url = "https://www.vimeo.com/video/123"
        with pytest.raises(ValueError, match="Unsupported URL"):
            download_video(url)

    @pytest.mark.unit
    @pytest.mark.medium
    def test_download_with_custom_output_path(self):
        """Test downloading with custom output path."""
        # TODO: Implement actual test when functionality is available
        # url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        # output_path = "test_data/custom_video.mp4"
        # video_path = download_video(url, output_path)
        # assert video_path == output_path or Path(output_path).exists()
        # pytest.skip("Requires yt-dlp installation")

    @pytest.mark.unit
    @pytest.mark.medium
    def test_get_video_info_tiktok(self):
        """Test getting video info from TikTok."""
        # TODO: Implement actual test when functionality is available
        # url = "https://www.tiktok.com/@user/video/123"
        # info = get_video_info(url)
        # assert "title" in info or "id" in info
        # pytest.skip("Requires real TikTok URL and yt-dlp installation")

    @pytest.mark.unit
    @pytest.mark.medium
    def test_get_video_info_youtube(self):
        """Test getting video info from YouTube."""
        # TODO: Implement actual test when functionality is available
        # url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        # info = get_video_info(url)
        # assert "title" in info
        # assert "duration" in info
        # pytest.skip("Requires yt-dlp installation")

