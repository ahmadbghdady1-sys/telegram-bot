import time
import google.generativeai as genai
import requests

TELEGRAM_TOKEN = "8612660334:AAF8-atRkQiThq4I-9bHnkXkTex3BIo097s"

GEMINI_API_KEY = "AIzaSyA8Hu3jUB8KyZnSjDF41v5FYLhx6vb2QGM"
TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/"

# إعداد مكتبة غوغل الرسمية
genai.configure(api_key=GEMINI_API_KEY)


def ask_gemini(prompt):
  try:
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    return response.text
  except Exception as e:
    return f"⚠️ خطأ من Google: {str(e)}"


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
  
