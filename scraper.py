# scraper.py — Fetches text content from a URL (article or YouTube)

import requests
import urllib3
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ─── HELPER FUNCTION ──────────────────────────────────────────────────────────

def is_youtube_url(url):
    """Check if the given URL is a YouTube link"""
    return "youtube.com/watch" in url or "youtu.be/" in url


# ─── YOUTUBE SCRAPER ──────────────────────────────────────────────────────────

def get_youtube_transcript(url):
    """Extract transcript text from a YouTube video URL"""
    
    try:
        # Extract the video ID from the URL
        if "youtube.com/watch" in url:
            video_id = url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in url:
            video_id = url.split("youtu.be/")[1].split("?")[0]
        else:
            return None, "Could not extract YouTube video ID."

        # Fetch the transcript (version 0.7.x method)
        ytt_api = YouTubeTranscriptApi()
        fetched = ytt_api.fetch(video_id, languages=['en', 'hi', 'mr', 'en-US', 'en-GB'])
        # Join all transcript pieces into one block of text
        full_transcript = " ".join([entry.text for entry in fetched])
        
        if not full_transcript.strip():
            return None, "Transcript is empty."
        
        return full_transcript, None

    except Exception as e:
        return None, f"YouTube error: {str(e)}"


# ─── ARTICLE SCRAPER ──────────────────────────────────────────────────────────

def get_article_text(url):
    """Extract clean readable text from a regular article URL"""
    
    try:
        # Set headers to pretend we are a real browser
        headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}
        
        
        # Fetch the webpage
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        
        # Check if request was successful
        if response.status_code != 200:
            return None, f"Failed to reach the page. Status code: {response.status_code}"
        
        # Parse the HTML
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Remove junk elements (ads, navbars, footers, scripts)
        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "form"]):
            tag.decompose()
        
        # Extract all paragraph text
        paragraphs = soup.find_all("p")
        text = " ".join([p.get_text() for p in paragraphs])
        
        # Clean up extra whitespace
        text = " ".join(text.split())
        
        # Check if we actually got meaningful content
        if len(text) < 100:
            return None, "Could not extract enough text. The page might be paywalled or JavaScript-rendered."
        
        return text, None

    except requests.exceptions.ConnectionError:
        return None, "Connection error. Please check the URL or your internet connection."
    
    except requests.exceptions.Timeout:
        return None, "The request timed out. The website took too long to respond."
    
    except Exception as e:
        return None, f"Article scraping error: {str(e)}"


# ─── MAIN FUNCTION ────────────────────────────────────────────────────────────

def scrape(url):
    """
    Main function — detects URL type and returns extracted text.
    Returns: (text, error)
    If successful: (text_content, None)
    If failed:     (None, error_message)
    """
    
    print(f"\n🔍 Scraping URL: {url}")
    
    if is_youtube_url(url):
        print("📺 Detected: YouTube video")
        text, error = get_youtube_transcript(url)
    else:
        print("📰 Detected: Article / Webpage")
        text, error = get_article_text(url)
    
    if error:
        print(f"❌ Error: {error}")
        return None, error
    
    print(f"✅ Successfully extracted {len(text.split())} words")
    return text, None


# ─── TEST THE SCRAPER ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    test_url = input("Enter a URL to test the scraper: ").strip()
    text, error = scrape(test_url)
    
    if text:
        print("\n--- EXTRACTED TEXT PREVIEW (first 500 chars) ---")
        print(text[:500])
    else:
        print(f"\nFailed: {error}")