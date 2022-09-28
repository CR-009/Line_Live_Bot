from crawler import *
from linebot.models import *
from config import *
#使用quote進行中文轉碼
from urllib.parse import quote

def HOT_carousel(alt_text, title , PTT_http , Htitle,titles):
    
    contents = dict()
    contents['type'] = 'carousel'
    contents['contents'] = []
    i=0
    for title , PTT_http in zip(Htitle,titles) :
        if i<10:
            bubble = {
                        "type": "bubble",
                        "direction": "ltr",
                        "hero": {
                            "type": "image",
                            "url": "https://i.imgur.com/g6Na3D6.png",
                            "size": "full",
                            "aspectRatio": "20:13",
                            "aspectMode": "cover"
                        },
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "spacing": "sm",
                            "contents": [
                            {
                                "type": "text",
                                "text": title,
                                "weight": "bold",
                                "size": "3xl",
                                "wrap": True,
                                "contents": []
                            }
                            ]
                        },
                        "footer": {
                            "type": "box",
                            "layout": "vertical",
                            "spacing": "sm",
                            "contents": [
                            {
                                "type": "button",
                                "action": {
                                "type": "uri",
                                "label": "點擊前往",
                                "uri": PTT_http
                                }
                            }
                            ]
                        }
                        }
        contents['contents'].append(bubble)
        i+=1
    message = FlexSendMessage(alt_text=alt_text,contents=contents)
    return message






    

