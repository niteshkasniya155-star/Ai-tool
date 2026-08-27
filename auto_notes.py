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
    prompt = f"Write a comprehensive study notes post in Hindi for competitive exams on topic: '{topic}'. Include top 5 bullet points with clear explanations."
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    response = requests.post(url, json=payload, headers=headers)
    res_data = response.json()
    
    if "candidates" not in res_data:
        print("Gemini API Error Response:", res_data)
        raise Exception("Gemini API Error: Check API key in GitHub Secrets.")
        
    return "📚 Daily Exam Special Study Notes 📚\n\n" + res_data['candidates'][0]['content']['parts'][0]['text']

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    res = requests.post(url, json=payload)
    res_data = res.json()
    
    if res.status_code != 200:
        print("Telegram API Error Response:", res_data)
        raise Exception("Telegram API Error: Check Bot Admin Permissions.")

if __name__ == "__main__":
    notes = generate_notes()
    send_to_telegram(notes)
    print("Successfully posted to Telegram!")
