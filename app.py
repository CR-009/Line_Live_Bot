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
import json


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
    elif "功能" in msg:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="您好，\n目前可以查詢的功能如下:\n\n 1.新聞選單\n 2.PTT選單\n 3.焦點新聞\n 4.財經新聞\n 5.請輸入「搜尋 [空格] 關鍵字」，\n     查詢Youtube影片。\n 6.熱門看板\n 7.八卦板\n 8.租屋板\n 9.西斯板\n 10.蘆洲租屋\n\n請輸入關鍵字以查詢需要的資訊。")
        )

    elif "新聞選單" in msg:
        FlexMessage = json.load(open('news.json','r',encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('新聞選單',FlexMessage))

    elif "PTT選單" in msg:
        FlexMessage = json.load(open('PTT.json','r',encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('PTT選單',FlexMessage))

    elif "焦點新聞" in msg :
        message = point_news_crawler()
        line_bot_api.reply_message(event.reply_token, message)

    elif "財經新聞" in msg :
        message = finance_news_crawler()
        line_bot_api.reply_message(event.reply_token, message)

    elif '搜尋' in msg:
        keyword = msg
        message = youtube_vedio_parser(keyword)
        line_bot_api.reply_message(event.reply_token, message)
    
    elif '西斯板' in msg:
        message = PTT_Sex_crawler()
        line_bot_api.reply_message(event.reply_token, message)
    
    elif "熱門文章" in msg :
        message = PTT_HOT_crawler()
        line_bot_api.reply_message(
            event.reply_token,
            line_bot_api.reply_message(event.reply_token, message)
        )

    elif "八卦板" in msg :
        message = PTT_Gossiping_crawler()
        line_bot_api.reply_message(
            event.reply_token,
            line_bot_api.reply_message(event.reply_token, message)
        )
    
    elif "租屋板" in msg :
        message = PTT_Rent_crawler()
        line_bot_api.reply_message(
            event.reply_token,
            line_bot_api.reply_message(event.reply_token, message)
        )

    elif "蘆洲租屋" in msg :
        message = PTT_LURent_crawler()
        line_bot_api.reply_message(
            event.reply_token,
            line_bot_api.reply_message(event.reply_token, message)
        )

                
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請輸入「功能」關鍵字，查詢想要的資訊。")
        )
    

# 測試用ngrok
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)

# # 上傳用 Heroku
# if __name__ == "__main__":
#     port = int(os.environ.get('PORT', 5000))
#     app.run(host='0.0.0.0', port=port)

