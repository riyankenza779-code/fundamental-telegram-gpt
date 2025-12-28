from openai import OpenAI
import os
import requests

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def get_analysis():
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Kamu adalah analis fundamental XAUUSD."},
            {"role": "user", "content": "Berikan analisa fundamental XAUUSD hari ini secara ringkas dalam bahasa Indonesia."}
        ]
    )
    return response.choices[0].message.content

def send_telegram(text):
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

if __name__ == "__main__":
    analysis = get_analysis()
    send_telegram(analysis)
