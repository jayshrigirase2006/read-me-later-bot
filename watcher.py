# watcher.py — Monitors a webpage and alerts you when something changes

import requests
import os
import time
import schedule
import hashlib
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from emailer import send_email

load_dotenv()

# ─── GET PAGE TEXT ────────────────────────────────────────────────────────────

def get_page_text(url):
    """Fetch clean text from a webpage"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        if response.status_code != 200:
            return None, f"Failed to reach page. Status: {response.status_code}"
        
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        
        text = " ".join(soup.get_text().split())
        return text, None
    
    except Exception as e:
        return None, f"Error: {str(e)}"


# ─── GET SNAPSHOT FILENAME ────────────────────────────────────────────────────

def get_snapshot_path(url):
    """Create a safe filename from URL"""
    url_hash = hashlib.md5(url.encode()).hexdigest()[:10]
    os.makedirs("snapshots", exist_ok=True)
    return f"snapshots/{url_hash}.txt"


# ─── SAVE SNAPSHOT ────────────────────────────────────────────────────────────

def save_snapshot(url, text):
    """Save current page text to snapshot file"""
    path = get_snapshot_path(url)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"💾 Snapshot saved for: {url[:50]}...")


# ─── LOAD SNAPSHOT ────────────────────────────────────────────────────────────

def load_snapshot(url):
    """Load previously saved snapshot"""
    path = get_snapshot_path(url)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# ─── CHECK FOR CHANGES ────────────────────────────────────────────────────────

def check_for_changes(url):
    """Check if page has changed since last snapshot"""
    print(f"\n🔍 Checking: {url[:50]}...")
    
    # Get current page text
    current_text, error = get_page_text(url)
    if error:
        print(f"❌ Error fetching page: {error}")
        return
    
    # Load old snapshot
    old_text = load_snapshot(url)
    
    # First time checking — just save snapshot
    if old_text is None:
        save_snapshot(url, current_text)
        print("📸 First snapshot saved! Will alert you on future changes.")
        return
    
    # Compare old vs new
    if current_text == old_text:
        print("✅ No changes detected.")
    else:
        print("🚨 CHANGE DETECTED! Sending email alert...")
        
        # Save new snapshot
        save_snapshot(url, current_text)
        
        # Send email alert
        summary = {
            "bullets": [
                "- A change was detected on the page you are watching",
                "- The content has been updated since your last check",
                "- Visit the page to see what changed"
            ],
            "sentiment": "N/A",
            "reason": "This is a page change alert, not a sentiment analysis"
        }
        
        success, error = send_email(summary, url)
        if success:
            print("✅ Alert email sent!")
        else:
            print(f"❌ Email failed: {error}")


# ─── START WATCHING ───────────────────────────────────────────────────────────

def watch_url(url, interval_minutes=30):
    """Watch a URL and check for changes every X minutes"""
    
    print(f"\n👁️  Starting watcher for: {url}")
    print(f"⏰ Checking every {interval_minutes} minutes")
    print("Press Ctrl+C to stop watching\n")
    
    # Check immediately first
    check_for_changes(url)
    
    # Schedule regular checks
    schedule.every(interval_minutes).minutes.do(check_for_changes, url)
    
    # Keep running
    while True:
        schedule.run_pending()
        time.sleep(30)


# ─── TEST THE WATCHER ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    test_url = input("Enter a URL to watch: ").strip()
    interval = input("Check every how many minutes? (default 30): ").strip()
    
    if not interval:
        interval = 30
    else:
        interval = int(interval)
    
    watch_url(test_url, interval)