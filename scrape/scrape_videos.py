"""
Scrape video URLs from TikTok and YouTube.
"""
import re
from typing import List
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
    
    # For user profiles, we need to scrape
    # TODO: Implement Playwright scraping logic for user profiles
    # - Launch browser
    # - Navigate to URL
    # - Wait for content to load
    # - Extract video URLs from page
    # - Return list of URLs
    
    try:
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            try:
                page.goto(url, wait_until="networkidle", timeout=30000)
                
                # Wait for video links to load
                page.wait_for_selector('a[href*="/video/"]', timeout=10000)
                
                # Extract all video URLs
                video_urls = page.evaluate("""
                    () => {
                        const links = Array.from(document.querySelectorAll('a[href*="/video/"]'));
                        return links.map(link => {
                            const href = link.getAttribute('href');
                            return href.startsWith('http') ? href : 'https://www.tiktok.com' + href;
                        }).filter((url, index, self) => self.indexOf(url) === index);
                    }
                """)
                
                browser.close()
                return video_urls if video_urls else []
                
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


def scrape_youtube_videos(url: str) -> List[str]:
    """
    Scrape YouTube video URLs from a given page.
    
    Args:
        url: YouTube URL (single video, channel, or playlist)
        
    Returns:
        List of video URLs
        
    Raises:
        ValueError: If URL is not a valid YouTube URL
    """
    if not is_youtube_url(url):
        raise ValueError(f"Invalid YouTube URL: {url}")
    
    # If it's already a single video URL, return it
    if '/watch' in url or '/shorts/' in url:
        return [url]
    
    # For channels or playlists, we can use yt-dlp to get video URLs
    # TODO: Implement channel/playlist scraping
    # For now, return empty list for non-video URLs
    return []


def scrape_videos(url: str) -> List[str]:
    """
    Scrape video URLs from TikTok or YouTube.
    
    Args:
        url: TikTok or YouTube URL
        
    Returns:
        List of video URLs
        
    Raises:
        ValueError: If URL is not from a supported platform
    """
    if is_tiktok_url(url):
        return scrape_tiktok_videos(url)
    elif is_youtube_url(url):
        return scrape_youtube_videos(url)
    else:
        raise ValueError(f"Unsupported URL: {url}. Must be from TikTok or YouTube.")


if __name__ == "__main__":
    # TODO: Add main execution logic
    pass

