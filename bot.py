import time
import requests

TELEGRAM_TOKEN = "8612660334:AAF8-atRkQiThq4I-9bHnkXkTex3BIo097s"
GEMINI_API_KEY = "AQ.Ab8RN6Kty6IDc8_okZ8czDouLTSQkeEL82ZrDVdlGnC7c2v2sg"
TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/"


def ask_gemini(prompt):
  url = "https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent"
  headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {GEMINI_API_KEY}",
  }
  payload = {"contents": [{"parts": [{"text": prompt}]}]}
  try:
    response = requests.post(url, json=payload, headers=headers)
    res_json = response.json()
    if response.status_code == 200 and "candidates" in res_json:
      return res_json["candidates"][0]["content"]["parts"][0]["text"]
    elif "error" in res_json:
      return f"⚠️ خطأ من Google: {res_json['error'].get('message', '')}"
    else:
      return f"⚠️ استجابة غير متوقعة: {res_json}"
  except Exception as e:
    return f"⚠️ خطأ: {str(e)}"


def get_updates(offset=None):
  url = TELEGRAM_URL + "getUpdates?timeout=30"
  if offset:
    url += f"&offset={offset}"
  try:
    return requests.get(url).json()
  except:
    return {}


def send_message(text, chat_id):
  requests.post(
      TELEGRAM_URL + "sendMessage", json={"chat_id": chat_id, "text": text}
  )


print("Bot is starting on Render...")
last_update_id = None
while True:
  updates = get_updates(last_update_id)
  if "result" in updates and updates["result"]:
    for update in updates["result"]:
      last_update_id = update["update_id"] + 1
      message = update.get("message", {})
      chat_id = message.get("chat", {}).get("id")
      text = message.get("text", "")

      if text == "/start":
        reply = "أهلاً بك! يعمل البوت الآن بنجاح على سيرفر دائم."
      elif text:
        reply = ask_gemini(text)
      else:
        reply = "يرجى إرسال نص."

      if chat_id:
        send_message(reply, chat_id)
  time.sleep(1)
  
