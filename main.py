from openai import OpenAI
import os
import requests

# === INIT OPENAI CLIENT ===
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# === ANALISIS GPT ===
def get_analysis():
    response = client.responses.create(
        model="gpt-4.1-mini",
        input="""
Buat analisa fundamental XAUUSD hari ini secara ringkas dan profesional (maksimal 4 poin).

WAJIB mencakup:
1. Kondisi USD dan arah kebijakan Federal Reserve terbaru
2. Inflasi AS dan ekspektasi suku bunga
3. Geopolitik global sebagai faktor safe haven
4. Jika sedang mendekati, berlangsung, atau baru selesai FOMC:
   - Sikap pasar
   - Potensi dampak keputusan FOMC ke XAUUSD
   - Bias XAUUSD (Bullish / Bearish / Netral)

Gunakan bahasa Indonesia, ringkas, tanpa rekomendasi entry.
"""
    )
    return response.output_text

# === KIRIM KE TELEGRAM ===
def send_telegram(text):
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, json={
        "chat_id": chat_id,
        "text": text
    })

# === MAIN EXECUTION ===
if __name__ == "__main__":
    analysis = get_analysis()
    send_telegram(analysis)
