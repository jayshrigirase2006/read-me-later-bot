# app.py — Flask web interface for Read-Me-Later Bot

from flask import Flask, render_template, request, jsonify
from scraper import scrape
from summarizer import summarize
from emailer import send_email
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)


# ─── HOME PAGE ────────────────────────────────────────────────────────────────

@app.route("/")
def home():
    return render_template("index.html")


# ─── SUMMARIZE ROUTE ──────────────────────────────────────────────────────────

@app.route("/summarize", methods=["POST"])
def summarize_url():
    data = request.get_json()
    url = data.get("url", "").strip()
    send_mail = data.get("send_email", False)
    
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    
    # Scrape
    text, error = scrape(url)
    if error:
        return jsonify({"error": f"Scraping failed: {error}"}), 400
    
    # Summarize
    summary, error = summarize(text)
    if error:
        return jsonify({"error": f"Summarizing failed: {error}"}), 400
    
    # Send email if requested
    if send_mail:
        send_email(summary, url)
    
    return jsonify({
        "bullets": summary["bullets"],
        "sentiment": summary["sentiment"],
        "reason": summary["reason"]
    })


if __name__ == "__main__":
    app.run(debug=True)