#呼叫自己的功能函數
from config import *
from Function import *
from crawler import *

#導入python的函數
import os
from flask import Flask, request, abort, render_template
from linebot.models import *
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError


app = Flask(__name__)
# Channel Access Token
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
# Channel Secret
handler = WebhookHandler(CHANNEL_SECRET)

# handle request from "/callback" 
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body      = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# handle text message
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text

    if "你好" in msg:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="您好，\n請問今天要查詢什麼呢?")
        )
    elif "新聞選單" in msg:
        message = news_list()
        line_bot_api.reply_message(event.reply_token, message)

    elif 'YT,' in msg:
        keyword = msg.split(',')[1]
        message = youtube_vedio_parser(keyword)
        line_bot_api.reply_message(event.reply_token, message)

                
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="輸入錯誤，請重新輸入。")
        )
    

#測試用ngrok
# if __name__ == "__main__":
#     port = int(os.environ.get('PORT', 80))
#     app.run(host='0.0.0.0', port=port)

# 上傳用 Heroku
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

