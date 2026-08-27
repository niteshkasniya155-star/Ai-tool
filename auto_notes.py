import os
import random
import requests
import google.generativeai as genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "").strip()

EXAMS = [
    "REET Exam Level 2 - Indian Geography Important One-Liners",
    "SSC CGL - General Awareness Top 10 Repeated Questions",
    "Railway RRB NTPC - Science Most Expected Questions",
    "Rajasthan Police Constable - Current Affairs & GK Notes"
]

def generate_notes():
    if not GEMINI_API_KEY:
        raise Exception("Gemini API Key missing hai! GitHub Secrets check karein.")
        
    # Google ki official library se API configuration (No URL/Headers headache)
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    topic = random.choice(EXAMS)
    prompt = f"Write a comprehensive study notes post in Hindi for competitive exams on topic: '{topic}'. Include top 5 bullet points with clear explanations."
    
    print("Google SDK library ke through request bhej rahe hain...")
    try:
        response = model.generate_content(prompt)
        return "📚 **Daily Exam Special Study Notes** 📚\n\n" + response.text
    except Exception as e:
        print("🚨 GEMINI SDK ERROR:")
        print(str(e))
        raise Exception("Google API Error! Upar error message padhein.")

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
