from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv

load_dotenv()
CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")

app = Flask(__name__)

def get_auto_reply(user_text):
    user_text = user_text.lower().strip()
    if "สวัสดี" in user_text:
        return "สวัสดีค่ะ 😊 มีอะไรให้ช่วยมั้ยคะ"
    elif "ราคา" in user_text:
        return "สามารถดูราคาได้ที่เว็บไซต์ของเรานะคะ www.example.com"
    elif "ติดต่อ" in user_text:
        return "สามารถติดต่อเราได้ที่เบอร์ 02-xxx-xxxx ค่ะ"
    else:
        return "ขอบคุณที่ติดต่อค่ะ ทีมงานจะตอบกลับเร็วที่สุด!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    try:
        user_text = data['events'][0]['message']['text']
        reply_token = data['events'][0]['replyToken']
        auto_reply = get_auto_reply(user_text)

        headers = {
            "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {
            "replyToken": reply_token,
            "messages": [{"type": "text", "text": auto_reply}]
        }

        requests.post("https://api.line.me/v2/bot/message/reply", headers=headers, json=payload)

    except Exception as e:
        print("❌ ERROR:", e)

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(port=5000)
