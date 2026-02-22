# summarizer.py — Sends text to Groq AI and gets summary + sentiment score

from groq import Groq
from dotenv import load_dotenv
import os

# Load secret keys from .env file
load_dotenv()


# ─── BUILD PROMPT ─────────────────────────────────────────────────────────────

def build_prompt(text):
    trimmed_text = text[:10000]
    
    prompt = f"""
You are a helpful summarization assistant.

Read the following content carefully and respond in EXACTLY this format:

BULLETS:
- [First key point from the content]
- [Second key point from the content]
- [Third key point from the content]

SENTIMENT: [score]/10
REASON: [One sentence explaining the tone or mood of the content]

Content to summarize:
{trimmed_text}
"""
    return prompt


# ─── PARSE RESPONSE ───────────────────────────────────────────────────────────

def parse_response(response_text):
    try:
        lines = response_text.strip().split("\n")
        
        bullets = []
        sentiment = ""
        reason = ""
        
        for line in lines:
            line = line.strip()
            if line.startswith("- "):
                bullets.append(line)
            elif line.startswith("SENTIMENT:"):
                sentiment = line.replace("SENTIMENT:", "").strip()
            elif line.startswith("REASON:"):
                reason = line.replace("REASON:", "").strip()
        
        return {
            "bullets": bullets,
            "sentiment": sentiment,
            "reason": reason
        }
    
    except Exception as e:
        return None


# ─── MAIN SUMMARIZE FUNCTION ──────────────────────────────────────────────────

def summarize(text):
    print("\n🤖 Sending text to Groq AI...")
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None, "Groq API key not found. Please check your .env file."
    
    try:
        client = Groq(api_key=api_key)
        
        prompt = build_prompt(text)
        
        response = client.chat.completions.create(
           model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        response_text = response.choices[0].message.content
        
        summary = parse_response(response_text)
        
        if not summary or not summary["bullets"]:
            return None, "Could not parse response properly."
        
        print("✅ Summary received from Groq!")
        return summary, None
    
    except Exception as e:
        return None, f"Groq API error: {str(e)}"


# ─── DISPLAY SUMMARY ──────────────────────────────────────────────────────────

def display_summary(summary):
    print("\n" + "="*50)
    print("📋 SUMMARY")
    print("="*50)
    
    for bullet in summary["bullets"]:
        print(bullet)
    
    print("\n" + "-"*50)
    print(f"😊 SENTIMENT SCORE: {summary['sentiment']}")
    print(f"💬 REASON: {summary['reason']}")
    print("="*50)


# ─── TEST THE SUMMARIZER ──────────────────────────────────────────────────────

if __name__ == "__main__":
    from scraper import scrape
    
    test_url = input("Enter a URL to summarize: ").strip()
    
    text, error = scrape(test_url)
    if error:
        print(f"Scraping failed: {error}")
        exit()
    
    summary, error = summarize(text)
    if error:
        print(f"Summarizing failed: {error}")
        exit()
    
    display_summary(summary)