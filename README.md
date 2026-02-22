# 🤖 Read-Me-Later Bot

A Python bot that summarizes any article or YouTube video into 3 bullet points and emails the summary to you automatically.

## ✨ Features

- 📰 Summarize any article URL
- 📺 Summarize any YouTube video
- 😊 Sentiment score with reason
- 📧 Email summary to your Gmail
- 👁️ Watch any webpage for changes
- 🌐 Beautiful web interface

## 🖥️ Demo

Paste any URL → Get instant AI summary → Receive it in your email!

## 🛠️ Tech Stack

- Python 3
- Flask — Web interface
- BeautifulSoup4 — Web scraping
- Groq API — AI summarization
- youtube-transcript-api — YouTube transcripts
- smtplib — Email sending
- schedule — Automatic page monitoring

## ⚙️ Setup Instructions

### 1. Clone the repository
```
git clone https://github.com/jayshrigirase2006/read-me-later-bot.git
cd read-me-later-bot
```

### 2. Create virtual environment
```
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

### 4. Create `.env` file
```
GEMINI_API_KEY=your_gemini_key
GROQ_API_KEY=your_groq_key
EMAIL_ADDRESS=your_gmail@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
RECEIVER_EMAIL=your_gmail@gmail.com
```

### 5. Run the web app
```
python app.py
```
Open browser at `http://127.0.0.1:5000`

### 6. Or run terminal version
```
python main.py
```

## 📁 Project Structure
```
read-me-later-bot/
│
├── main.py          → Terminal interface
├── scraper.py       → Fetches text from URLs
├── summarizer.py    → Groq AI summarization
├── emailer.py       → Gmail email sender
├── watcher.py       → Page change monitor
├── app.py           → Flask web interface
├── templates/
│   └── index.html   → Web UI design
├── snapshots/       → Saved page snapshots
├── .env             → Secret keys (never share)
├── requirements.txt → All dependencies
└── README.md        → This file
```

## 🔑 API Keys Needed

- **Groq API** — Free at https://console.groq.com
- **Gmail App Password** — https://myaccount.google.com/apppasswords

## 👨‍💻 Author

Made by Jayshri Girase