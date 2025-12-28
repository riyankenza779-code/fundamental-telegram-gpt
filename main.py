from openai import OpenAI
import os
import requests
from datetime import datetime

# =========================
# INIT
# =========================
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# =========================
# SESSION DETECTION
# =========================
hour_utc = datetime.utcnow().hour
if hour_utc < 7:
    session = "PAGI (Asia Session)"
else:
    session = "MALAM (US Session)"

# =========================
# ANALISIS GPT (LEVEL 5 + 6)
# =========================
def get_analysis():
    prompt = f"""
Kamu adalah analis makro profesional.

Buat UPDATE FUNDAMENTAL {session} dengan format SUPER RINGKAS (maksimal 4 poin + emoji).

PAIR WAJIB:
🟡 XAUUSD
💶 EURUSD
₿ BTCUSD

WAJIB LOGIC EVENT:
- Jika H-1 FOMC → tulis **PRE-FOMC ALERT**
- Jika hari FOMC → tulis **FOMC DAY – POTENSI VOLATILITAS**
- Jika pasca FOMC → tulis **POST-FOMC IMPACT**
- Jika tidak ada FOMC → tulis **NO MAJOR FED EVENT**

ATURAN ISI:
- Maksimal 4 poin TOTAL
- Setiap poin boleh membahas lebih dari satu pair
- Sertakan bias singkat (Bullish / Bearish / Netral)
- Bahasa Indonesia
- Fokus dampak ke harga
- Tanpa entry / SL / TP

FORMAT WAJIB:
📊 Fundamental Update

1️⃣ 🟡 XAUUSD: ...
2️⃣ 💶 EURUSD: ...
3️⃣ ₿ BTCUSD: ...
4️⃣ 🔔 Event: ...
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text

# =========================
# SEND TELEGRAM
# =========================
def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(
        url,
        json={
            "chat_id": CHAT_ID,
            "text": text
        }
    )

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    analysis = get_analysis()
    send_telegram(analysis)
