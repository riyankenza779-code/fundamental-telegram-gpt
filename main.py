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
# DETECT SESSION (PAGI / MALAM)
# =========================
hour_utc = datetime.utcnow().hour
if hour_utc < 7:
    session = "PAGI (Asia Session)"
else:
    session = "MALAM (US Session)"

# =========================
# ANALISIS GPT
# =========================
def get_analysis():
    prompt = f"""
Kamu adalah analis market profesional.

Buat UPDATE FUNDAMENTAL {session} dengan format SUPER RINGKAS (maksimal 4 poin + emoji).

WAJIB bahas:
🟡 XAUUSD (emas)
💶 EURUSD
₿ BTCUSD

ATURAN ISI:
- Maksimal 4 poin total (bukan per pair)
- Setiap poin boleh membahas lebih dari 1 pair
- Jika mendekati / hari H / pasca FOMC → WAJIB disebut
- Sertakan bias singkat (Bullish / Bearish / Netral)
- Bahasa Indonesia
- Tanpa rekomendasi entry

CONTOH FORMAT:
📊 Fundamental Update

1️⃣ 🟡 XAUUSD: ...
2️⃣ 💶 EURUSD: ...
3️⃣ ₿ BTCUSD: ...
4️⃣ 🔔 Event (FOMC / CPI / NFP): ...
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
