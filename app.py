import os
from crawler import *
from linebot.models import *
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from flask import Flask, request, abort, render_template
from picture_search import *
import random

app = Flask(__name__)

Channel_Access_Token = 'iSMOZduFbHkTglNwWIKqaYgzO9B9LL0VpcdV4/1QEgbYrNekuQSJBxDV5yi9yoLquDizYjeux4NZBHOUTx3rwxcSFZaDw+tixor0ZtoUMuFrSipfQZb+JLOY50s8IcF6PAYRwUaJywp9oaN2sz03MgdB04t89/1O/w1cDnyilFU='
line_bot_api    = LineBotApi(Channel_Access_Token)
Channel_Secret  = '1d60146099c8460565358a489b0a0524'
handler = WebhookHandler(Channel_Secret)


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

    if "焦點新聞" in msg :
        result = point_news_crawler()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=result)
        )

    elif "財經新聞" in msg :
        result = finance_news_crawler()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=result)
        )
    elif "sex" in msg:
        result = sex_crawler()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=result)
        )

    elif "圖片"in msg:
        result = pic_find(event)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=result)
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="暫時不支援，請重新輸入。")
        )


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
