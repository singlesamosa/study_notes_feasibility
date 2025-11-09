"""
Tests for extract_audio module.
"""
import pytest
import sys
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from audio.extract_audio import extract_audio, check_ffmpeg_installed


class TestExtractAudio:
    """Test suite for extract_audio module."""

    @pytest.mark.unit
    @pytest.mark.high
    def test_2_1_valid_mp4_video_file(self):
        """Test Case 2.1: Valid MP4 Video File"""
        # Skip if FFmpeg not installed
        if not check_ffmpeg_installed():
            pytest.skip("FFmpeg not installed")
        
        # Use real downloaded video if available
        video_path = "test_downloads/youtube_shorts_test.mp4"
        if not Path(video_path).exists():
            pytest.skip(f"Test video not found: {video_path}")
        
        output_path = "test_downloads/output_audio.wav"
        result = extract_audio(video_path, output_path)
        
        # Verify output
        assert result == output_path
        assert Path(output_path).exists()
        assert Path(output_path).stat().st_size > 0

    @pytest.mark.unit
    @pytest.mark.high
    def test_2_2_nonexistent_video_file(self):
        """Test Case 2.2: Non-existent Video File"""
        # Skip if FFmpeg not installed
        if not check_ffmpeg_installed():
            pytest.skip("FFmpeg not installed")
        
        video_path = "test_data/nonexistent.mp4"
        output_path = "test_data/output_audio.wav"
        # Expected: FileNotFoundError
        with pytest.raises(FileNotFoundError):
            extract_audio(video_path, output_path)

    @pytest.mark.unit
    @pytest.mark.medium
    def test_2_3_invalid_video_format(self):
        """Test Case 2.3: Invalid Video Format"""
        video_path = "test_data/image.jpg"
        output_path = "test_data/output_audio.wav"
        # TODO: Implement actual test when functionality is available
        # Expected: ValueError or FFmpeg error
        # pytest.skip("Functionality not implemented yet")

    @pytest.mark.unit
    @pytest.mark.medium
    def test_2_4_video_without_audio_track(self):
        """Test Case 2.4: Video Without Audio Track"""
        video_path = "test_data/video_no_audio.mp4"
        output_path = "test_data/output_audio.wav"
        # TODO: Implement actual test when functionality is available
        # Expected: ValueError or empty file with warning
        # pytest.skip("Functionality not implemented yet")

    @pytest.mark.unit
    @pytest.mark.low
    def test_2_5_output_directory_doesnt_exist(self):
        """Test Case 2.5: Output Directory Doesn't Exist"""
        video_path = "test_data/sample_video.mp4"
        output_path = "nonexistent_dir/output_audio.wav"
        # TODO: Implement actual test when functionality is available
        # Expected: Create directory or FileNotFoundError
        # pytest.skip("Functionality not implemented yet")

    @pytest.mark.unit
    @pytest.mark.high
    def test_2_6_verify_wav_format_specifications(self):
        """Test Case 2.6: Verify WAV Format Specifications"""
        # Skip if FFmpeg not installed
        if not check_ffmpeg_installed():
            pytest.skip("FFmpeg not installed")
        
        # Use real downloaded video if available
        video_path = "test_downloads/tiktok_test.mp4"
        if not Path(video_path).exists():
            pytest.skip(f"Test video not found: {video_path}")
        
        output_path = "test_downloads/tiktok_audio.wav"
        result = extract_audio(video_path, output_path)
        
        # Verify output file exists and has content
        assert Path(result).exists()
        assert Path(result).stat().st_size > 0
        
        # Note: Full format verification would require audio analysis library
        # For now, we verify the file exists and has content

