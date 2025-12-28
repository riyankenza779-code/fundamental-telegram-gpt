from openai import OpenAI
import os
import requests

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def get_analysis():
    response = client.responses.create(
        model="gpt-4.1-mini",
        input="Berikan analisa fundamental XAUUSD hari ini secara ringkas, fokus USD, Fed, inflasi, dan geopolitik."
    )
    return response.output_text

def send_telegram(text):
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, json={
        "chat_id": chat_id,
        "text": text
    })

if __name__ == "__main__":
    analysis = get_analysis()
    send_telegram(analysis)
