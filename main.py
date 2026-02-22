# main.py — The manager that connects everything together

from scraper import scrape
from summarizer import summarize, display_summary
from emailer import send_email
from watcher import watch_url
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# ─── MAIN MENU ────────────────────────────────────────────────────────────────

def show_menu():
    print("\n" + "="*50)
    print("🤖 READ-ME-LATER BOT")
    print("="*50)
    print("1. Summarize a URL")
    print("2. Watch a URL for changes")
    print("3. Exit")
    print("="*50)


# ─── SUMMARIZE MODE ───────────────────────────────────────────────────────────

def summarize_mode():
    url = input("\n🔗 Enter URL to summarize: ").strip()
    
    if not url:
        print("❌ No URL entered!")
        return
    
    # Step 1 - Scrape
    text, error = scrape(url)
    if error:
        print(f"❌ Scraping failed: {error}")
        return
    
    # Step 2 - Summarize
    summary, error = summarize(text)
    if error:
        print(f"❌ Summarizing failed: {error}")
        return
    
    # Step 3 - Display
    display_summary(summary)
    
    # Step 4 - Ask to email
    send = input("\n📧 Send summary to your email? (y/n): ").strip().lower()
    if send == "y":
        success, error = send_email(summary, url)
        if error:
            print(f"❌ Email failed: {error}")
        else:
            print("🎉 Check your Gmail inbox!")


# ─── WATCH MODE ───────────────────────────────────────────────────────────────

def watch_mode():
    url = input("\n🔗 Enter URL to watch: ").strip()
    
    if not url:
        print("❌ No URL entered!")
        return
    
    interval = input("⏰ Check every how many minutes? (default 30): ").strip()
    
    if not interval:
        interval = 30
    else:
        interval = int(interval)
    
    watch_url(url, interval)


# ─── MAIN LOOP ────────────────────────────────────────────────────────────────

def main():
    print("\n🚀 Welcome to Read-Me-Later Bot!")
    
    while True:
        show_menu()
        choice = input("\nEnter your choice (1/2/3): ").strip()
        
        if choice == "1":
            summarize_mode()
        elif choice == "2":
            watch_mode()
        elif choice == "3":
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice! Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()