import os
import requests
import openai
import datetime

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

openai.api_key = OPENAI_API_KEY

def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    })

today = datetime.date.today().strftime("%d %B %Y")

prompt = f"""
Kamu adalah analis makroekonomi & emas profesional.

Buat laporan FUNDAMENTAL HARIAN (ringkas, bahasa Indonesia) untuk tanggal {today}.

Fokus:
- Ekonomi US
- Eurozone
- China

Tampilkan:
• Ringkasan makro (maks 3 poin)
• Sentimen pasar
• Dampak USD
• Dampak XAU/USD
• Bias XAU/USD

Gunakan format singkat (1 layar Telegram).
"""

response = openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
)

analysis = response.choices[0].message.content
send_telegram(analysis)
