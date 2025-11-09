#!/usr/bin/env python3
"""
Example script to test video downloading from TikTok and YouTube.
"""
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from download.download_video import download_video, get_video_info, is_tiktok_url, is_youtube_url


def test_youtube_download():
    """Test downloading a YouTube video."""
    print("=" * 60)
    print("Testing YouTube Video Download")
    print("=" * 60)
    
    # Use a well-known YouTube video (Rick Roll - always available)
    youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    print(f"\n1. Testing URL detection...")
    assert is_youtube_url(youtube_url), "Should detect YouTube URL"
    print("   ✅ YouTube URL detected correctly")
    
    print(f"\n2. Getting video info...")
    try:
        info = get_video_info(youtube_url)
        print(f"   ✅ Video info retrieved")
        print(f"   Title: {info.get('title', 'N/A')}")
        print(f"   Duration: {info.get('duration', 'N/A')} seconds")
        print(f"   Uploader: {info.get('uploader', 'N/A')}")
    except Exception as e:
        print(f"   ⚠️  Could not get video info: {e}")
    
    print(f"\n3. Downloading video...")
    try:
        output_path = "test_downloads/youtube_test.mp4"
        video_path = download_video(youtube_url, output_path)
        print(f"   ✅ Video downloaded successfully!")
        print(f"   Path: {video_path}")
        
        # Check if file exists
        if Path(video_path).exists():
            file_size = Path(video_path).stat().st_size
            print(f"   File size: {file_size / (1024*1024):.2f} MB")
        else:
            print(f"   ⚠️  File not found at expected path")
            
    except Exception as e:
        print(f"   ❌ Download failed: {e}")
        print(f"   This might be expected if yt-dlp has issues or network problems")


def test_tiktok_download():
    """Test downloading a TikTok video."""
    print("\n" + "=" * 60)
    print("Testing TikTok Video Download")
    print("=" * 60)
    
    # You'll need to provide a real TikTok URL
    print("\n⚠️  To test TikTok download, provide a real TikTok URL")
    print("   Example: https://www.tiktok.com/@username/video/1234567890")
    
    # Uncomment and add a real TikTok URL to test:
    # tiktok_url = "https://www.tiktok.com/@username/video/1234567890"
    # 
    # print(f"\n1. Testing URL detection...")
    # assert is_tiktok_url(tiktok_url), "Should detect TikTok URL"
    # print("   ✅ TikTok URL detected correctly")
    # 
    # print(f"\n2. Downloading video...")
    # try:
    #     output_path = "test_downloads/tiktok_test.mp4"
    #     video_path = download_video(tiktok_url, output_path)
    #     print(f"   ✅ Video downloaded successfully!")
    #     print(f"   Path: {video_path}")
    # except Exception as e:
    #     print(f"   ❌ Download failed: {e}")


def test_platform_detection():
    """Test platform detection."""
    print("\n" + "=" * 60)
    print("Testing Platform Detection")
    print("=" * 60)
    
    test_urls = [
        ("https://www.youtube.com/watch?v=123", "YouTube"),
        ("https://youtu.be/123", "YouTube"),
        ("https://www.youtube.com/shorts/123", "YouTube"),
        ("https://www.tiktok.com/@user/video/123", "TikTok"),
        ("https://tiktok.com/@user/video/123", "TikTok"),
    ]
    
    for url, expected_platform in test_urls:
        is_youtube = is_youtube_url(url)
        is_tiktok = is_tiktok_url(url)
        
        if expected_platform == "YouTube":
            assert is_youtube, f"Should detect {url} as YouTube"
            assert not is_tiktok, f"Should not detect {url} as TikTok"
            print(f"   ✅ {url[:50]}... → YouTube")
        else:
            assert is_tiktok, f"Should detect {url} as TikTok"
            assert not is_youtube, f"Should not detect {url} as YouTube"
            print(f"   ✅ {url[:50]}... → TikTok")


if __name__ == "__main__":
    print("\n🧪 Testing Video Download Functionality\n")
    
    # Create test downloads directory
    Path("test_downloads").mkdir(exist_ok=True)
    
    try:
        # Test platform detection
        test_platform_detection()
        
        # Test YouTube download
        test_youtube_download()
        
        # Test TikTok download (commented out - needs real URL)
        test_tiktok_download()
        
        print("\n" + "=" * 60)
        print("✅ All tests completed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

