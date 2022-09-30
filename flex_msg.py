from crawler import *
from linebot.models import *
from config import *
#使用quote進行中文轉碼
from urllib.parse import quote

#YT 旋轉Flex Message
def yt_carousel(alt_text,image_url_list,vedio_url_list,title_list,yt_channel_infos_image_urls,yt_channel_infos_names):
    contents = dict()
    contents['type'] = 'carousel'
    contents['contents'] = []
    i=0
    for image_url, vedio_url, title, channel_img, channel_name in zip(image_url_list,vedio_url_list,title_list,yt_channel_infos_image_urls,yt_channel_infos_names):
        if i<10:
            bubble =    {   "type": "bubble",
                            "hero": {
                                "type": "image",
                                "url": image_url + '?',
                                "size": "full",
                                "aspectRatio": "16:9",
                                "aspectMode": "cover",
                                "action": {
                                "type": "uri",
                                "uri": vedio_url
                                }
                            },
                            "body": {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": title[:30] if len(title)<30 else title[:30] + '...',
                                    "size": "sm",
                                    "wrap": True,
                                    "contents": []
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                    {
                                        "type": "image",
                                        "url": channel_img + '?',
                                        "animated": True,
                                        "size": "xxs",
                                        "align": "start",
                                        "flex": 0,
                                        "aspectMode": "cover"
                                    },
                                    {
                                        "type": "text",
                                        "text": channel_name,
                                        "size": "xs",
                                        "align": "start",
                                        "gravity": "center",
                                        "margin": "md"
                                    }
                                    ],
                                    "margin": "md"
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
                                    "style": "primary",
                                    "height": "sm",
                                    "action": {
                                    "type": "uri",
                                    "label": "點擊前往",
                                    "uri":  vedio_url,
                                    }
                                }
                                ],
                                "flex": 0
                            }
                            }
            contents['contents'].append(bubble)
            i+=1
    message = FlexSendMessage(alt_text=alt_text,contents=contents)
    return message

# #Sex 旋轉Flex Message
# def Sex_carousel(alt_text,Stitle,sex_http,sex_title_list,sex_https_list):
#     contents = dict()
#     contents['type'] = 'carousel'
#     contents['contents'] = []
#     i=0
#     for Stitle,sex_http in zip(sex_title_list,sex_https_list):
#         if i<10:
#             bubble = {
#                         "type": "bubble",
#                         "direction": "ltr",
#                         "hero": {
#                             "type": "image",
#                             "url": "https://i.imgur.com/EhqYOr0.png",
#                             "size": "full",
#                             "aspectRatio": "20:13",
#                             "aspectMode": "cover",
#                             "action": {
#                             "type": "uri",
#                             "uri": sex_http
#                             }
#                         },
#                         "body": {
#                             "type": "box",
#                             "layout": "vertical",
#                             "spacing": "sm",
#                             "contents": [
#                             {
#                                 "type": "text",
#                                 "text": Stitle,
#                                 "weight": "bold",
#                                 "size": "xl",
#                                 "wrap": True,
#                                 "contents": []
#                             }
#                             ]
#                         },
#                         "footer": {
#                             "type": "box",
#                             "layout": "vertical",
#                             "spacing": "sm",
#                             "contents": [
#                             {
#                                 "type": "button",
#                                 "action": {
#                                 "type": "uri",
#                                 "label": "點擊前往",
#                                 "uri": sex_http
#                                 }
#                             }
#                             ]
#                         }
#                         }

#             contents['contents'].append(bubble)
#             i+=1
#     message = FlexSendMessage(alt_text=alt_text,contents=contents)
#     return contents

