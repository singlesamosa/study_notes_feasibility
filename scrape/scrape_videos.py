"""
Scrape video URLs from TikTok and YouTube.
"""
import re
import subprocess
import json
from typing import List, Optional, Union
from urllib.parse import urlparse, parse_qs

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
except ImportError:
    pass  # Playwright not installed yet


def is_tiktok_url(url: str) -> bool:
    """Check if URL is a TikTok URL."""
    return "tiktok.com" in url.lower()


def is_youtube_url(url: str) -> bool:
    """Check if URL is a YouTube URL."""
    youtube_patterns = [
        r'youtube\.com',
        r'youtu\.be',
        r'youtube\.com/watch',
        r'youtube\.com/shorts'
    ]
    return any(re.search(pattern, url.lower()) for pattern in youtube_patterns)


def scrape_tiktok_videos(url: str) -> List[str]:
    """
    Scrape TikTok video URLs from a given page.
    
    Args:
        url: TikTok page URL (single video or user profile)
        
    Returns:
        List of video URLs
        
    Raises:
        ValueError: If URL is not a valid TikTok URL
        ConnectionError: If network request fails
    """
    if not is_tiktok_url(url):
        raise ValueError(f"Invalid TikTok URL: {url}")
    
    # If it's already a single video URL, return it
    if '/video/' in url:
        return [url]
    
    # For user profiles, we need to scrape using Playwright
    # Try multiple approaches: Playwright scraping or yt-dlp
    
    # First, try using yt-dlp to get video URLs (more reliable)
    try:
        import subprocess
        yt_dlp_cmd = None
        try:
            subprocess.run(["yt-dlp", "--version"], capture_output=True, check=True)
            yt_dlp_cmd = "yt-dlp"
        except:
            try:
                subprocess.run(["python3", "-m", "yt_dlp", "--version"], capture_output=True, check=True)
                yt_dlp_cmd = ["python3", "-m", "yt_dlp"]
            except:
                pass
        
        if yt_dlp_cmd:
            # Use yt-dlp to get video URLs from TikTok channel
            cmd = [yt_dlp_cmd] if isinstance(yt_dlp_cmd, str) else yt_dlp_cmd
            cmd.extend([
                "--flat-playlist",
                "--print", "url",
                "--no-warnings",
                url
            ])
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                video_urls = []
                for line in result.stdout.strip().split('\n'):
                    line = line.strip()
                    if line and line.startswith('http') and 'tiktok.com' in line:
                        video_urls.append(line)
                
                if video_urls:
                    # Remove duplicates
                    seen = set()
                    unique_urls = []
                    for url_item in video_urls:
                        if url_item not in seen:
                            seen.add(url_item)
                            unique_urls.append(url_item)
                    return unique_urls
    except Exception:
        pass  # Fall back to Playwright
    
    # Fallback to Playwright scraping
    try:
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            try:
                # Increase timeout and wait for page to load
                page.goto(url, wait_until="domcontentloaded", timeout=60000)
                
                # Wait a bit for dynamic content to load
                page.wait_for_timeout(3000)
                
                # Try multiple selectors for video links
                selectors = [
                    'a[href*="/video/"]',
                    '[data-e2e="user-post-item"] a',
                    'a[href*="video"]'
                ]
                
                video_urls = []
                for selector in selectors:
                    try:
                        page.wait_for_selector(selector, timeout=5000)
                        # Extract all video URLs
                        urls = page.evaluate(f"""
                            () => {{
                                const links = Array.from(document.querySelectorAll('{selector}'));
                                return links.map(link => {{
                                    const href = link.getAttribute('href');
                                    return href ? (href.startsWith('http') ? href : 'https://www.tiktok.com' + href) : null;
                                }}).filter(url => url && url.includes('/video/'));
                            }}
                        """)
                        video_urls.extend(urls if urls else [])
                        if video_urls:
                            break
                    except:
                        continue
                
                browser.close()
                
                # Remove duplicates and return
                seen = set()
                unique_urls = []
                for url_item in video_urls:
                    if url_item and url_item not in seen:
                        seen.add(url_item)
                        unique_urls.append(url_item)
                
                return unique_urls if unique_urls else []
                
            except PlaywrightTimeoutError:
                browser.close()
                raise ConnectionError(f"Timeout loading TikTok page: {url}")
            except Exception as e:
                browser.close()
                raise ConnectionError(f"Failed to scrape TikTok: {e}")
                
    except ImportError:
        raise ImportError("Playwright is required for TikTok scraping. Install with: pip install playwright && playwright install")
    except Exception as e:
        raise ConnectionError(f"Failed to scrape TikTok videos: {e}")


def scrape_youtube_videos(
    url: str,
    max_videos: Optional[Union[int, str]] = 10
) -> List[str]:
    """
    Scrape YouTube video URLs from a given page.
    
    Args:
        url: YouTube URL (single video, channel, or playlist)
        max_videos: Maximum number of videos to scrape. 
                   Default: 10
                   Use int for specific limit (e.g., 50)
                   Use "all" or None to get all videos (no limit)
        
    Returns:
        List of video URLs
        
    Raises:
        ValueError: If URL is not a valid YouTube URL or max_videos is invalid
        FileNotFoundError: If yt-dlp is not installed
        RuntimeError: If scraping fails
    """
    if not is_youtube_url(url):
        raise ValueError(f"Invalid YouTube URL: {url}")
    
    # If it's already a single video URL, return it
    if '/watch' in url or '/shorts/' in url:
        return [url]
    
    # For channels or playlists, use yt-dlp to get video URLs
    # Check if yt-dlp is available
    yt_dlp_cmd = None
    try:
        subprocess.run(["yt-dlp", "--version"], capture_output=True, check=True)
        yt_dlp_cmd = "yt-dlp"
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            subprocess.run(["python3", "-m", "yt_dlp", "--version"], capture_output=True, check=True)
            yt_dlp_cmd = ["python3", "-m", "yt_dlp"]
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise FileNotFoundError(
                "yt-dlp is not installed. Install it with: pip install yt-dlp"
            )
    
    # Determine playlist end parameter
    if max_videos is None or (isinstance(max_videos, str) and max_videos.lower() == "all"):
        playlist_end = None  # No limit
    elif isinstance(max_videos, int) and max_videos > 0:
        playlist_end = max_videos
    else:
        raise ValueError(
            f"Invalid max_videos value: {max_videos}. "
            f"Must be a positive integer or 'all'"
        )
    
    try:
        # Build yt-dlp command to extract video URLs
        # --flat-playlist: Don't download, just list videos
        # --get-url: Get video URLs
        # --playlist-end: Limit number of videos
        cmd = [yt_dlp_cmd] if isinstance(yt_dlp_cmd, str) else yt_dlp_cmd
        cmd.extend([
            "--flat-playlist",
            "--print", "url",  # Print video URLs
            "--no-warnings",
            "--no-playlist-reverse",  # Get latest videos first
        ])
        
        # Add playlist end limit if specified
        if playlist_end is not None:
            cmd.extend(["--playlist-end", str(playlist_end)])
        
        # Add the URL
        cmd.append(url)
        
        # Run yt-dlp
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            timeout=60  # 60 second timeout
        )
        
        # Parse output - each line is a video URL
        video_urls = []
        for line in result.stdout.strip().split('\n'):
            line = line.strip()
            if line and line.startswith('http'):
                # Ensure it's a full YouTube URL
                if 'youtube.com' in line or 'youtu.be' in line:
                    video_urls.append(line)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_urls = []
        for url_item in video_urls:
            if url_item not in seen:
                seen.add(url_item)
                unique_urls.append(url_item)
        
        # Apply limit if specified (yt-dlp may return more than requested)
        if playlist_end is not None and len(unique_urls) > playlist_end:
            unique_urls = unique_urls[:playlist_end]
        
        return unique_urls
        
    except subprocess.TimeoutExpired:
        raise RuntimeError(f"Timeout while scraping YouTube videos from: {url}")
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr or e.stdout or "Unknown error"
        
        # Check for common errors
        if "Private video" in error_msg or "Video unavailable" in error_msg:
            raise ValueError(f"Some videos are unavailable or private: {url}")
        elif "This video is not available" in error_msg:
            raise ValueError(f"Video/channel not available: {url}")
        else:
            raise RuntimeError(f"Failed to scrape YouTube videos: {error_msg}")
    except Exception as e:
        raise RuntimeError(f"Failed to scrape YouTube videos: {e}")


def scrape_videos(
    url: str,
    max_videos: Optional[Union[int, str]] = 10
) -> List[str]:
    """
    Scrape video URLs from TikTok or YouTube.
    
    Args:
        url: TikTok or YouTube URL
        max_videos: Maximum number of videos to scrape (YouTube channels/playlists only).
                   Default: 10
                   Use int for specific limit (e.g., 50)
                   Use "all" or None to get all videos (no limit)
                   Note: For TikTok, this parameter is ignored (always returns all found)
        
    Returns:
        List of video URLs
        
    Raises:
        ValueError: If URL is not from a supported platform
    """
    if is_tiktok_url(url):
        return scrape_tiktok_videos(url)
    elif is_youtube_url(url):
        return scrape_youtube_videos(url, max_videos=max_videos)
    else:
        raise ValueError(f"Unsupported URL: {url}. Must be from TikTok or YouTube.")


if __name__ == "__main__":
    # TODO: Add main execution logic
    pass

