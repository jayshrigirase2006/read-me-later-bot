# emailer.py — Sends summary email to your Gmail

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()


# ─── FORMAT EMAIL BODY ────────────────────────────────────────────────────────

def format_email_body(summary, url):
    """Format the summary nicely for email"""
    
    bullets = "\n".join(summary["bullets"])
    
    body = f"""
📰 Read-Me-Later Summary Bot
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔗 URL: {url}

📋 SUMMARY:
{bullets}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
😊 SENTIMENT SCORE: {summary["sentiment"]}
💬 REASON: {summary["reason"]}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Sent by your Read-Me-Later Bot 🤖
"""
    return body


# ─── SEND EMAIL ───────────────────────────────────────────────────────────────

def send_email(summary, url):
    """Send summary email using Gmail SMTP"""
    
    print("\n📧 Sending email...")
    
    # Get credentials from .env
    sender_email = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")
    receiver_email = os.getenv("RECEIVER_EMAIL")
    
    if not sender_email or not password or not receiver_email:
        return False, "Email credentials not found in .env file."
    
    try:
        # Create email message
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = "📚 Your Read-Me-Later Summary is Ready!"
        
        # Format and attach body
        body = format_email_body(summary, url)
        msg.attach(MIMEText(body, "plain"))
        
        # Connect to Gmail SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        
        # Login
        server.login(sender_email, password)
        
        # Send email
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        
        print(f"✅ Email sent successfully to {receiver_email}!")
        return True, None
    
    except smtplib.SMTPAuthenticationError:
        return False, "Gmail authentication failed. Check your email and app password in .env file."
    
    except smtplib.SMTPException as e:
        return False, f"SMTP error: {str(e)}"
    
    except Exception as e:
        return False, f"Email error: {str(e)}"


# ─── TEST THE EMAILER ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    from scraper import scrape
    from summarizer import summarize, display_summary
    
    test_url = input("Enter a URL to summarize and email: ").strip()
    
    # Step 1 - Scrape
    text, error = scrape(test_url)
    if error:
        print(f"Scraping failed: {error}")
        exit()
    
    # Step 2 - Summarize
    summary, error = summarize(text)
    if error:
        print(f"Summarizing failed: {error}")
        exit()
    
    # Step 3 - Display
    display_summary(summary)
    
    # Step 4 - Send Email
    success, error = send_email(summary, test_url)
    if error:
        print(f"Email failed: {error}")
    else:
        print("\n🎉 Check your Gmail inbox!")