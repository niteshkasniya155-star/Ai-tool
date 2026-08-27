import os
import random
import requests
import json

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "").strip()
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "").strip()

EXAMS = [
    "REET Exam Level 2 - Indian Geography Important One-Liners",
    "SSC CGL - General Awareness Top 10 Repeated Questions",
    "Railway RRB NTPC - Science Most Expected Questions",
    "Rajasthan Police Constable - Current Affairs & GK Notes"
]

def generate_notes():
    if not GROQ_API_KEY:
        raise Exception("Groq API Key missing hai! GitHub Secrets check karein.")
        
    topic = random.choice(EXAMS)
    prompt = f"Write a comprehensive study notes post in Hindi for competitive exams on topic: '{topic}'. Include top 5 bullet points with clear explanations."
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    
    print("Groq AI ko request bhej rahe hain...")
    response = requests.post(url, json=payload, headers=headers)
    result = response.json()
    
    if 'choices' not in result:
        print("🚨 GROQ API ERROR:")
        print(json.dumps(result, indent=2))
        raise Exception("Groq API Error! Logs check karein.")
        
    return "📚 **Daily Exam Special Study Notes** 📚\n\n" + result['choices'][0]['message']['content']

def send_to_telegram(text):
    print("Telegram par message bhej rahe hain...")
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    response = requests.post(url, json=payload)
    
    if response.status_code != 200:
        print("🚨 TELEGRAM API ERROR:")
        print(response.text)
        raise Exception("Telegram posting fail ho gayi.")

if __name__ == "__main__":
    notes = generate_notes()
    send_to_telegram(notes)
    print("✅ SUCCESS! Notes Telegram par successfully post ho gaye.")
