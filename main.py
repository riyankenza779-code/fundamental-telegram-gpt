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
session = "PAGI (Asia Session)" if hour_utc < 7 else "MALAM (US Session)"

# =========================
# SEND TELEGRAM
# =========================
def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": text
    })

# =========================
# GLOBAL MODE ANALYSIS (LEVEL 12)
# =========================
def get_global_mode():
    prompt = f"""
Tentukan GLOBAL MARKET MODE hari ini (RISK-ON / RISK-OFF / NEUTRAL).

Berdasarkan:
- Federal Reserve & ekspektasi suku bunga
- Inflasi AS & yield obligasi
- Sentimen risiko global & geopolitik
- China (PBoC) dan ECB

Lalu jelaskan:
- Penyebab utama (maksimal 3 poin)
- Implikasi singkat untuk:
  🟡 XAUUSD
  💶 EURUSD
  ₿ BTCUSD

FORMAT:
🌍 GLOBAL MARKET MODE: ...

Penyebab:
- ...
- ...
- ...

Implikasi:
🟡 XAUUSD: ...
💶 EURUSD: ...
₿ BTCUSD: ...
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )
    return response.output_text

# =========================
# PRE-FOMC ALERT CHECK (LEVEL 13)
# =========================
def check_pre_fomc():
    prompt = """
Apakah BESOK ada pengumuman kebijakan suku bunga Federal Reserve (FOMC)?

Jawab dengan format TEGAS:
- Jika YA, tulis:
  YES
  lalu buat pesan ALERT singkat (3–4 baris) tentang potensi dampak ke XAUUSD, EURUSD, dan BTC.
- Jika TIDAK, jawab:
  NO
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    text = response.output_text.strip()
    if text.startswith("YES"):
        return "🚨 PRE-FOMC ALERT (H-1)\n\n" + text.replace("YES", "").strip()
    return None

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    # 1️⃣ Kirim Global Market Mode (rutin)
    global_update = get_global_mode()
    send_telegram(f"📊 {session}\n\n{global_update}")

    # 2️⃣ Kirim PRE-FOMC ALERT jika ada
    alert = check_pre_fomc()
    if alert:
        send_telegram(alert)
