import requests
from bs4 import BeautifulSoup
from flex_mes import *

#財經新聞
def finance_news_crawler():
    base = "https://news.cnyes.com"
    url  = "https://news.cnyes.com/news/cat/headline"
    re   = requests.get(url)

    contentfn = ""

    soup = BeautifulSoup(re.text, "html.parser")
    data = soup.find_all("a", {"class": "_1Zdp"})
    
    for indexfn, d in enumerate(data):
        if indexfn <5:
            title = d.text
            hreffn  = base + d.get("href")
            contentfn += "{}\n{}\n".format(title, hreffn)
            
        else:
            continue
        
    return contentfn

#焦點新聞
def point_news_crawler():

    url = "https://tw.yahoo.com/"
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}

    list_req = requests.get(url,headers=headers)
    soup = BeautifulSoup(list_req.content, "html.parser")

    news_list = soup.find_all('a',{"class":"Fz(16px) LineClamp(1,20px) Fw(700) Td(n) Td(u):h C(#324fe1) V(h) active_V(v)"})
    contentpn = ""

    for indexpn, pointdata in enumerate(news_list):
        if indexpn <5:
            title = pointdata.text
            hrefpn  = pointdata.get("href")
            contentpn += "{}\n{}\n".format(title, hrefpn)
        else:
            break
        
    return contentpn

#PTT-熱門看板
def PTT_HOT_crawler():
    
    url="https://disp.cc/b/PttHot"
    my_headers = {'cookie':'over18=1'}
    response = requests.get(url,headers=my_headers)
    soup = BeautifulSoup(response.text, "html.parser")
    titles = soup.find_all('span','L34 nowrap listTitle')

    # contentHOT = ""
    contents = dict()
    contents['type'] = 'carousel'
    contents['contents'] = []
    i=0
    for index,Htitle in enumerate(titles):
        if index < 10:
            if Htitle.a != None:
                title = Htitle.text
                PTT_href  = Htitle.select_one("a").get("href")
                PTT_base = "https://disp.cc/b/"
                PTT_http = PTT_base + PTT_href
                # contentHOT += "{}\n{}\n\n".format(title,PTT_http)
                # # print(contentHOT)
        
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
            index+=1
    message = FlexSendMessage(alt_text="熱門看板",contents=contents)

    return message


#PTT-西斯板
def PTT_Sex_crawler():
    
    url="https://www.ptt.cc/bbs/Sex/index.html"
    my_headers = {'cookie':'over18=1'}
    response = requests.get(url,headers=my_headers)
    soup = BeautifulSoup(response.text, "html.parser")
    titles = soup.find_all('div','title')
    
    # contentSex = ""
    contents = dict()
    contents['type'] = 'carousel'
    contents['contents'] = []
    i=0
    for index,Stitle in enumerate(titles):
        if index < 10:
            if Stitle.a != None:
                title = Stitle.text
                PTT_href  = Stitle.select_one("a").get("href")
                PTT_base = "https://www.ptt.cc/"
                PTT_http = PTT_base + PTT_href
                # contentSex += "{}\n{}\n\n".format(title,PTT_http)
                # print(contentSex)
                
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
            index+=1
    message = FlexSendMessage(alt_text="sex",contents=contents)

    return message

#PTT-八卦版
def PTT_Gossiping_crawler():
    
    url="https://www.ptt.cc/bbs/Gossiping/index.html"
    my_headers = {'cookie':'over18=1'}
    response = requests.get(url,headers=my_headers)
    soup = BeautifulSoup(response.text, "html.parser")
    titles = soup.find_all('div','title')
   
    contentGossiping = ""

    for index,Gtitle in enumerate(titles):
        if index < 8:
            if Gtitle.a != None:
                title = Gtitle.text
                PTT_href  = Gtitle.select_one("a").get("href")
                PTT_http = "https://www.ptt.cc/"
                contentGossiping += "{}\n{}\n".format(title,PTT_http + PTT_href)
                # print(contentGossiping)


#PTT-租屋板-蘆洲
def PTT_LURent_crawler():
    
    url="https://www.ptt.cc/bbs/Rent_apart/search?q=%E8%98%86%E6%B4%B2"
    my_headers = {'cookie':'over18=1'}
    response = requests.get(url,headers=my_headers)
    soup = BeautifulSoup(response.text, "html.parser")
    titles = soup.find_all('div','title')
    
    contentLURent= ""
   
    for index,LUrenttitle in enumerate(titles):
        if LUrenttitle.a != None:
            title = LUrenttitle.text
            PTT_href  = LUrenttitle.select_one("a").get("href")
            PTT_http = "https://www.ptt.cc/"
            contentLURent += "{}\n{}\n".format(title,PTT_http + PTT_href)
            print(contentLURent)
                
        else:
            break
 
    return contentLURent

#PTT-租屋板
def PTT_Rent_crawler():
    
    url="https://www.ptt.cc/bbs/Rent_apart/index.html"
    my_headers = {'cookie':'over18=1'}
    response = requests.get(url,headers=my_headers)
    soup = BeautifulSoup(response.text, "html.parser")
    titles = soup.find_all('div','title')
    
    contentRent= ""
   
    for index,renttitle in enumerate(titles):
        if renttitle.a != None:
            title = renttitle.text
            PTT_href  = renttitle.select_one("a").get("href")
            PTT_http = "https://www.ptt.cc/"
            contentRent += "{}\n{}\n".format(title,PTT_http + PTT_href)
            print(contentRent)
                
        else:
            break
 
    return contentRent

