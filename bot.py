import os
import time
import sys
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8850100988:AAG_dykth10VoIhdY4X7ehiVKA14_6HeKGU")

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")

if GROQ_API_KEY and GROQ_API_KEY.startswith("Gsk_"):
    GROQ_API_KEY = "gsk_" + GROQ_API_KEY[4:]

TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

def ask_groq(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "أنت مساعد ذكي ومحترف، تجيب بدقة ووضوح باللغة العربية."},
            {"role": "user", "content": prompt}
        ]
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=20)
        res_json = response.json()
        if response.status_code == 200 and "choices" in res_json:
            return res_json["choices"][0]["message"]["content"]
        elif "error" in res_json:
            return f"⚠️ خطأ Groq: {res_json['error'].get('message', 'حدث خطأ غير معروف')}"
        else:
            return f"⚠️ استجابة غير متوقعة: {res_json}"
    except Exception as e:
        return f"⚠️ خطأ في الاتصال: {str(e)}"

def send_message(chat_id, text):
    url = TELEGRAM_URL + "/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Error sending message: {e}", flush=True)

def main():
    print("Starting bot main loop...", flush=True)
    try:
        r = requests.get(TELEGRAM_URL + "/deleteWebhook")
        print(f"Delete Webhook status: {r.text}", flush=True)
    except Exception as e:
        print(f"Delete webhook error: {e}", flush=True)

    offset = None
    print("Bot is running and listening for messages...", flush=True)
    while True:
        try:
            url = TELEGRAM_URL + "/getUpdates?timeout=30"
            if offset:
                url += f"&offset={offset}"
            
            res = requests.get(url, timeout=35).json()
            if res.get("ok"):
                for result in res.get("result", []):
                    offset = result["update_id"] + 1
                    message = result.get("message", {})
                    chat_id = message.get("chat", {}).get("id")
                    text = message.get("text", "")
                    
                    if chat_id and text:
                        print(f"Received message from {chat_id}: {text}", flush=True)
                        reply = ask_groq(text)
                        send_message(chat_id, reply)
                        print(f"Sent reply to {chat_id}", flush=True)
            else:
                print(f"Telegram response not ok: {res}", flush=True)
                time.sleep(3)
        except Exception as e:
            print(f"Loop error: {e}", flush=True)
            time.sleep(3)

if __name__ == "__main__":
    main()
    
