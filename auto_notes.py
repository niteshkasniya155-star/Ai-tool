import os
import random
import requests
import json

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
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    print("Gemini API ko request bhej rahe hain...")
    response = requests.post(url, json=payload, headers=headers)
    result = response.json()
    
    if 'candidates' not in result:
        print("🚨 GEMINI API ERROR:")
        print(json.dumps(result, indent=2))
        raise Exception("API Key invalid hai ya Secrets me set nahi hai. Upar logs check karein.")
        
    return "📚 **Daily Exam Special Study Notes** 📚\n\n" + result['candidates'][0]['content']['parts'][0]['text']

def send_to_telegram(text):
    print("Telegram par message bhej rahe hain...")
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    response = requests.post(url, json=payload)
    
    if response.status_code != 200:
        print("🚨 TELEGRAM API ERROR:")
        print(json.dumps(response.json(), indent=2))
        raise Exception("Telegram posting fail ho gayi. Bot Admin access ya Chat ID check karein.")

if __name__ == "__main__":
    notes = generate_notes()
    send_to_telegram(notes)
    print("✅ SUCCESS! Notes Telegram par successfully post ho gaye.")
