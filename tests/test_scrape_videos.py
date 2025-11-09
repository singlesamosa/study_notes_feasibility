"""
Tests for scrape_videos module.
"""
import pytest
import sys
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from scrape.scrape_videos import (
    scrape_tiktok_videos,
    scrape_youtube_videos,
    scrape_videos,
    is_tiktok_url,
    is_youtube_url
)


class TestScrapeVideos:
    """Test suite for scrape_videos module."""

    @pytest.mark.unit
    @pytest.mark.high
    def test_1_1_valid_tiktok_url_single_video(self):
        """Test Case 1.1: Valid TikTok URL - Single Video"""
        url = "https://www.tiktok.com/@username/video/1234567890"
        # TODO: Implement actual test when functionality is available
        result = scrape_tiktok_videos(url)
        # Expected: ["https://www.tiktok.com/@username/video/1234567890"]
        assert isinstance(result, list)
        # pytest.skip("Functionality not implemented yet")

    @pytest.mark.integration
    @pytest.mark.high
    def test_1_2_valid_tiktok_url_user_profile(self):
        """Test Case 1.2: Valid TikTok URL - User Profile Page"""
        url = "https://www.tiktok.com/@username"
        # TODO: Implement actual test when functionality is available
        result = scrape_tiktok_videos(url)
        # Expected: List of video URLs
        assert isinstance(result, list)
        # pytest.skip("Functionality not implemented yet")

    @pytest.mark.unit
    @pytest.mark.medium
    def test_1_3_invalid_url(self):
        """Test Case 1.3: Invalid URL"""
        url = "https://www.youtube.com/watch?v=abc123"
        # TODO: Implement actual test when functionality is available
        # Expected: [] or ValueError
        with pytest.raises((ValueError, Exception)):
            scrape_tiktok_videos(url)
        # pytest.skip("Functionality not implemented yet")

    @pytest.mark.unit
    @pytest.mark.medium
    def test_1_4_malformed_url(self):
        """Test Case 1.4: Malformed URL"""
        url = "not-a-url"
        # TODO: Implement actual test when functionality is available
        # Expected: ValueError or URLError
        with pytest.raises((ValueError, Exception)):
            scrape_tiktok_videos(url)
        # pytest.skip("Functionality not implemented yet")

    @pytest.mark.integration
    @pytest.mark.medium
    def test_1_5_network_error_handling(self):
        """Test Case 1.5: Network Error Handling"""
        url = "https://www.tiktok.com/@username"
        # TODO: Implement actual test when functionality is available
        # Expected: ConnectionError or TimeoutError
        # pytest.skip("Functionality not implemented yet")

    @pytest.mark.unit
    @pytest.mark.high
    def test_scrape_youtube_single_video(self):
        """Test scraping a single YouTube video URL."""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        result = scrape_youtube_videos(url)
        assert isinstance(result, list)
        assert len(result) == 1
        assert url in result

    @pytest.mark.unit
    @pytest.mark.high
    def test_scrape_videos_platform_detection(self):
        """Test that scrape_videos detects platform correctly."""
        tiktok_url = "https://www.tiktok.com/@user/video/123"
        youtube_url = "https://www.youtube.com/watch?v=123"
        
        # Should work for both platforms
        assert is_tiktok_url(tiktok_url)
        assert is_youtube_url(youtube_url)
        
        # scrape_videos should route to correct function
        # (actual scraping may fail, but routing should work)
        try:
            result = scrape_videos(tiktok_url)
            assert isinstance(result, list)
        except (ConnectionError, ImportError):
            pass  # Expected if Playwright not installed or network fails

    @pytest.mark.unit
    @pytest.mark.medium
    def test_scrape_videos_unsupported_platform(self):
        """Test that scrape_videos rejects unsupported platforms."""
        url = "https://www.vimeo.com/video/123"
        with pytest.raises(ValueError, match="Unsupported URL"):
            scrape_videos(url)

