import os
import random
import requests

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

EXAMS = [
    "REET Exam Level 2 - Indian Geography Important One-Liners",
    "SSC CGL - General Awareness Top 10 Repeated Questions",
    "Railway RRB NTPC - Science Most Expected Questions",
    "Rajasthan Police Constable - Current Affairs & GK Notes"
]

def generate_notes():
    topic = random.choice(EXAMS)
    prompt = f"Write a comprehensive, highly readable study notes post in Hindi (Hinglish/Hindi mixed) for competitive exams on topic: '{topic}'. Include top 5-7 key bullet points with clear explanations."
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    response = requests.post(url, json=payload, headers=headers)
    result = response.json()
    return f"📚 **Daily Exam Special Study Notes** 📚\n\n" + result['candidates'][0]['content']['parts'][0]['text']

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

if __name__ == "__main__":
    notes = generate_notes()
    send_to_telegram(notes)
