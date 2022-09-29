#功能列表
#導入Line BOT 模組
from linebot.models import *
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

#1.建立旋轉木馬訊息，名為function_list(未來可以叫出此函數來使用)
#function_list的括號內是設定此函數呼叫時需要給函數的參數有哪些

def news_list():
    contents = {
        "contents": [
            {
            "type": "bubble",
            "size": "mega",
            "direction": "ltr",
            "hero": {
                "type": "image",
                "url": "https://i.imgur.com/FllfPCv.png",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
                "action": {
                "type": "message",
                "label": "焦點新聞",
                "text": "焦點新聞"
                }
            },
            "styles": {
                "hero": {
                "separator": True
                }
            }
            },
            {
            "type": "bubble",
            "size": "mega",
            "direction": "ltr",
            "action": {
                "type": "message",
                "label": "財經新聞",
                "text": "財經新聞"
            },
            "hero": {
                "type": "image",
                "url": "https://i.imgur.com/giWLwAk.png",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
                "action": {
                "type": "message",
                "label": "焦點新聞",
                "text": "焦點新聞"
                }
            }
            }
        ]
        }
        
    return message