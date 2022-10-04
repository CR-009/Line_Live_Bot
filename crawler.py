from selenium import webdriver
from selenium.webdriver.common.by import By
from linebot.models import *
from flex_msg import *
from config import *
import time
import random
import string
from bs4 import BeautifulSoup
import requests
from urllib.parse import quote 


# YT_關鍵字搜尋
def youtube_vedio_parser(keyword):

    url = 'https://tw.youtube.com/'

    #建立chrome設定
    chromeOption = webdriver.ChromeOptions()
    #設定瀏覽器的user agent
    # chromeOption.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0')
    chromeOption.add_argument("start-maximized")
    chromeOption.add_argument('--headless')
    chromeOption.add_argument('--no-sandbox')
    chromeOption.add_argument('--disable-dev-shm-usage')
    #開啟Chrome瀏覽器
    driver = webdriver.Chrome(options=chromeOption)
    #調整瀏覽器視窗大小
    driver.set_window_size(1024, 960)

     #======================依關鍵字在youtube網站上搜尋===========================
    #進入指定網址
    driver.get(url)
    #定義一個物件，以name標籤找到youtube的關鍵字搜尋欄位
    search_vedio = driver.find_element(By.NAME,'search_query')
    #將關鍵字文字送入搜尋欄位
    search_vedio.send_keys(keyword)
    time.sleep(1)

     #按下輸入搜尋按鈕
#    search_vedio.send_keys(Keys.RETURN)
    search_button = driver.find_element(By.ID,'search-icon-legacy')
    search_button.click()
    #等待網頁讀取
    time.sleep(1)


    #======================存取搜尋到的結果的螢幕截圖===========================
    #在static資料夾中建立一個暫存圖片路徑
    # image_path = './static/tmp/test.png'

    # #刷新網頁 => 移除首頁的元素
    driver.refresh()
    # #將目前的頁面截圖儲存至暫存圖片路徑
    # driver.save_screenshot(image_path)
    #休息2秒
    time.sleep(2)

 #======================從網頁獲取前十個影片連結===========================
    #建立影片url列表
    vedio_url_list = []
    #以css選擇器搜尋youtube的影片連結    
    yt_vedio_urls = driver.find_elements(By.CSS_SELECTOR,'.ytd-thumbnail')
    #將每個影片連結放入連結list
    #print(len(yt_vedio_urls))
    for url in yt_vedio_urls:
        #print(url.get_attribute('href'))
        if len(vedio_url_list)<10:
            if url.get_attribute('href')!=None:
                vedio_url_list.append(url.get_attribute('href'))

    
    #======================從網頁獲得影片的前十張縮圖===========================
    #滾動視窗捲軸，使瀏覽器獲取影片縮圖資訊
    for i in range(50):
        y_position = i*100
        driver.execute_script(f'window.scrollTo(0, {y_position});')
        time.sleep(0.1)
    
    #建立縮圖列表
    yt_vedio_images = []
    yt_vedio_images_urls = driver.find_elements(By.CSS_SELECTOR,'.yt-simple-endpoint.inline-block.style-scope.ytd-thumbnail yt-img-shadow img#img')

    #將每個圖片的縮圖放入圖片list-
    for image in yt_vedio_images_urls:
        if str(type(image.get_attribute('src'))) != "<class 'NoneType'>":
            if 'ytimg' in image.get_attribute('src') or '720.jpg?' in image.get_attribute('src') or 'hqdefault.jpg?' in image.get_attribute('src'):
                if len(yt_vedio_images)<10:
                    yt_vedio_images.append(image.get_attribute('src'))
                    # print(image.get_attribute('src'))
    

    #======================從網頁獲取前十個影片標題===========================
    #建立標題列表
    yt_title_list = []
    yt_vedio_infos = driver.find_elements(By.CSS_SELECTOR,'#video-title.ytd-video-renderer')
    for infos in yt_vedio_infos:
        yt_title_list.append(infos.get_attribute('title'))
        # print(infos.get_attribute('title'))

    #===================從網頁獲取前十個發布者頻道資訊========================
    #建立頻道資訊列表(圖片)
    yt_channel_infos_image_urls = []
    yt_channel_infos_image_list = driver.find_elements(By.CSS_SELECTOR,'#channel-info a yt-img-shadow #img')
    for infos in yt_channel_infos_image_list:
        yt_channel_infos_image_urls.append(infos.get_attribute('src'))
        # print(infos.get_attribute('src'))

    #建立頻道資訊列表(頻道名稱)
    yt_channel_infos_names = []
    yt_channel_infos_name_list = driver.find_elements(By.CSS_SELECTOR,'#channel-info ytd-channel-name div#container div#text-container yt-formatted-string a')
    for infos in yt_channel_infos_name_list:
        yt_channel_infos_names.append(infos.text)

    #關閉瀏覽器連線
    driver.close()

  #==============將爬取到的資訊以FlexMessage回傳至主程式===================
    message = []   
            
    #瀏覽器螢幕截圖-下面三行關掉就不會有螢幕截圖傳送過來
    #建立一個隨機4碼的字串，使圖片縮圖瀏覽不會因為讀取同一個url快取而重覆
    # random_code = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(4))
    # message.append(ImageSendMessage(original_content_url= HEROKU_APP_URL + '/static/tmp/test.png?'+random_code,preview_image_url= HEROKU_APP_URL + '/static/tmp/test.png?'+random_code))
    
    #回傳搜尋結果的FlexMessage
    message.append(yt_carousel('YT搜尋結果',yt_vedio_images,vedio_url_list,yt_title_list,yt_channel_infos_image_urls,yt_channel_infos_names))
    return message

#PTT-西斯板
def PTT_Sex_crawler():
    
    url="https://disp.cc/b/sex"
    my_headers = {'cookie':'over18=1'}
    response = requests.get(url,headers=my_headers)
    soup = BeautifulSoup(response.text, "html.parser")
    titles = soup.find_all('span','L34 nowrap listTitle')

    contents = dict()
    contents['type'] = 'carousel'
    contents['contents'] = []
    index=0
    for index,Stitle in enumerate(titles):
        if index < 10:
            if Stitle.a != None:
                title = Stitle.text
                PTT_href  = Stitle.select_one("a").get("href")
                PTT_base = "https://disp.cc/b/"
                PTT_http = PTT_base + PTT_href
        
                bubble = {
                        "type": "bubble",
                        "hero": {
                            "type": "image",
                            "url": "https://i.imgur.com/EhqYOr0.png",
                            "size": "full",
                            "aspectRatio": "20:13",
                            "aspectMode": "cover",
                            "action": {
                            "type": "uri",
                            "uri": PTT_http
                            }
                        },
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "text",
                                "text": title,
                                "weight": "bold",
                                "size": "xl",
                                "wrap": True
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
                                "style": "link",
                                "height": "sm",
                                "action": {
                                "type": "uri",
                                "label": "點擊前往",
                                "uri": PTT_http
                                }
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [],
                                "margin": "sm"
                            }
                            ],
                            "flex": 0
                        }
                        }
            contents['contents'].append(bubble)
            index+=1
    # print(contenthts)
    message = FlexSendMessage(alt_text="西斯板",contents=contents)

    return message

#財經新聞
def finance_news_crawler():
    base = "https://news.cnyes.com"
    url  = "https://news.cnyes.com/news/cat/headline"
    re   = requests.get(url)

    contentfn = ""

    soup = BeautifulSoup(re.text, "html.parser")
    data = soup.find_all("a", {"class": "_1Zdp"})

    contents = dict()
    contents['type'] = 'carousel'
    contents['contents'] = []
    index=0
    for index, d in enumerate(data):
        if index <10:
            title = d.text
            http  = base + d.get("href")
            # contentfn += "{}\n{}\n".format(title, hreffn)
            
            bubble = {
                        "type": "bubble",
                        "hero": {
                            "type": "image",
                            "url": "https://i.imgur.com/giWLwAk.png",
                            "size": "full",
                            "aspectRatio": "20:13",
                            "aspectMode": "cover",
                            "action": {
                            "type": "uri",
                            "uri": http
                            }
                        },
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "text",
                                "text": title,
                                "weight": "bold",
                                "size": "xl",
                                "wrap": True
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
                                "style": "link",
                                "height": "sm",
                                "action": {
                                "type": "uri",
                                "label": "點擊前往",
                                "uri": http
                                }
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [],
                                "margin": "sm"
                            }
                            ],
                            "flex": 0
                        }
                        }
            contents['contents'].append(bubble)
            index+=1
    # print(contents)
    message = FlexSendMessage(alt_text="財經新聞",contents=contents)

    return message

#焦點新聞
def point_news_crawler():

    url = "https://tw.yahoo.com/"
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}

    list_req = requests.get(url,headers=headers)
    soup = BeautifulSoup(list_req.content, "html.parser")

    news_list = soup.find_all('a',{"class":"Fz(16px) LineClamp(1,20px) Fw(700) Td(n) Td(u):h C(#324fe1) V(h) active_V(v)"})

    contents = dict()
    contents['type'] = 'carousel'
    contents['contents'] = []
    index=0
    for index,pointtitle in enumerate(news_list):
        if index < 10:
            title = pointtitle.text
            http  = pointtitle.get("href") 

            bubble = {
                        "type": "bubble",
                        "hero": {
                            "type": "image",
                            "url": "https://i.imgur.com/FllfPCv.png",
                            "size": "full",
                            "aspectRatio": "20:13",
                            "aspectMode": "cover",
                            "action": {
                            "type": "uri",
                            "uri": http
                            }
                        },
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "text",
                                "text": title,
                                "weight": "bold",
                                "size": "xl",
                                "wrap": True
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
                                "style": "link",
                                "height": "sm",
                                "action": {
                                "type": "uri",
                                "label": "點擊前往",
                                "uri": http
                                }
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [],
                                "margin": "sm"
                            }
                            ],
                            "flex": 0
                        }
                        }
            contents['contents'].append(bubble)
            index+=1
    # print(contents)
    message = FlexSendMessage(alt_text="熱門文章",contents=contents)

    return message

#PTT-熱門看板
def PTT_HOT_crawler():
    
    url="https://disp.cc/b/main"
    my_headers = {'cookie':'over18=1'}
    response = requests.get(url,headers=my_headers)
    soup = BeautifulSoup(response.text, "html.parser")
    titles = soup.find_all('span','ht_title')

    
    contents = dict()
    contents['type'] = 'carousel'
    contents['contents'] = []
    index=0
    for index,Stitle in enumerate(titles):
        if index < 10:
            if Stitle.a != None:
                title = Stitle.text
                PTT_href  = Stitle.select_one("a").get("href")
                PTT_base = "https://disp.cc/b/"
                PTT_http = PTT_base + PTT_href
        
                bubble = {
                        "type": "bubble",
                        "hero": {
                            "type": "image",
                            "url": "https://i.imgur.com/kylWAB8.png",
                            "size": "full",
                            "aspectRatio": "20:13",
                            "aspectMode": "cover",
                            "action": {
                            "type": "uri",
                            "uri": PTT_http
                            }
                        },
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "text",
                                "text": title,
                                "weight": "bold",
                                "size": "xl",
                                "wrap": True
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
                                "style": "link",
                                "height": "sm",
                                "action": {
                                "type": "uri",
                                "label": "點擊前往",
                                "uri": PTT_http
                                }
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [],
                                "margin": "sm"
                            }
                            ],
                            "flex": 0
                        }
                        }
            contents['contents'].append(bubble)
            index+=1
    # print(contents)
    message = FlexSendMessage(alt_text="熱門文章",contents=contents)

    return message

#PTT-八卦版
def PTT_Gossiping_crawler():
    
    url="https://disp.cc/b/Gossiping"
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    titles = soup.find_all('span','L34 nowrap listTitle')

    contents = dict()
    contents['type'] = 'carousel'
    contents['contents'] = []
    index=0
    for index,Gtitle in enumerate(titles):
        if index < 10:
            if Gtitle.a != None:
                title = Gtitle.text
                PTT_href  = Gtitle.select_one("a").get("href")
                PTT_base = "https://disp.cc/b/"
                PTT_http = PTT_base + PTT_href
                print(PTT_http)
        
                bubble = {  "type": "bubble",
                            "hero": {
                            "type": "image",
                            "url": "https://i.imgur.com/SY6xc3s.png",
                            "size": "full",
                            "aspectRatio": "20:13",
                            "aspectMode": "cover",
                            "action": {
                            "type": "uri",
                            "uri": PTT_http
                            }
                        },
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "text",
                                "text": title,
                                "weight": "bold",
                                "size": "xl",
                                "wrap": True
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
                                "style": "link",
                                "height": "sm",
                                "action": {
                                "type": "uri",
                                "label": "點擊前往",
                                "uri": PTT_http
                                }
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [],
                                "margin": "sm"
                            }
                            ],
                            "flex": 0
                        }
                        }
            contents['contents'].append(bubble)
            index+=1
    # print(contenthts)
    message = FlexSendMessage(alt_text="八卦板",contents=contents)

    return message

#PTT-租屋板-蘆洲
def PTT_LURent_crawler():
    
    url="https://www.ptt.cc/bbs/Rent_apart/search?q=%E8%98%86%E6%B4%B2"
    my_headers = {'cookie':'over18=1'}
    response = requests.get(url,headers=my_headers)
    soup = BeautifulSoup(response.text, "html.parser")
    titles = soup.find_all('div','title')
    contents = dict()
    contents['type'] = 'carousel'
    contents['contents'] = []
    index=0
    for index,Rtitle in enumerate(titles):
        if index < 10:
            if Rtitle.a != None:
                title = Rtitle.text
                PTT_href  = Rtitle.select_one("a").get("href")
                PTT_base = "https://www.ptt.cc/"
                PTT_http = PTT_base + PTT_href
                print(PTT_http)
        
                bubble = {  "type": "bubble",
                            "hero": {
                            "type": "image",
                            "url": "https://i.imgur.com/POfRi3G.png",
                            "size": "full",
                            "aspectRatio": "20:13",
                            "aspectMode": "cover",
                            "action": {
                            "type": "uri",
                            "uri": PTT_http
                            }
                        },
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "text",
                                "text": title,
                                "weight": "bold",
                                "size": "xl",
                                "wrap": True
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
                                "style": "link",
                                "height": "sm",
                                "action": {
                                "type": "uri",
                                "label": "點擊前往",
                                "uri": PTT_http
                                }
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [],
                                "margin": "sm"
                            }
                            ],
                            "flex": 0
                        }
                        }
            contents['contents'].append(bubble)
            index+=1
    # print(contents)
    message = FlexSendMessage(alt_text="蘆洲租屋",contents=contents)

    return message
# PTT_LURent_crawler()

#PTT-租屋板
def PTT_Rent_crawler():

    url="https://www.ptt.cc/bbs/Rent_apart/index.html"
    my_headers = {'cookie':'over18=1'}
    response = requests.get(url,headers=my_headers)
    soup = BeautifulSoup(response.text, "html.parser")
    titles = soup.find_all('div','title')
    contents = dict()
    contents['type'] = 'carousel'
    contents['contents'] = []
    index=0
    for index,Rtitle in enumerate(titles):
        if index < 10:
            if Rtitle.a != None:
                title = Rtitle.text
                PTT_href  = Rtitle.select_one("a").get("href")
                PTT_base = "https://www.ptt.cc/"
                PTT_http = PTT_base + PTT_href
                print(PTT_http)
        
                bubble = {  "type": "bubble",
                            "hero": {
                            "type": "image",
                            "url": "https://i.imgur.com/POfRi3G.png",
                            "size": "full",
                            "aspectRatio": "20:13",
                            "aspectMode": "cover",
                            "action": {
                            "type": "uri",
                            "uri": PTT_http
                            }
                        },
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "text",
                                "text": title,
                                "weight": "bold",
                                "size": "xl",
                                "wrap": True
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
                                "style": "link",
                                "height": "sm",
                                "action": {
                                "type": "uri",
                                "label": "點擊前往",
                                "uri": PTT_http
                                }
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [],
                                "margin": "sm"
                            }
                            ],
                            "flex": 0
                        }
                        }
            contents['contents'].append(bubble)
            index+=1
    # print(contents)
    message = FlexSendMessage(alt_text="租屋板",contents=contents)

    return message

#TFT-聯盟戰棋-波堤
def TFT_crawler():

    url = 'https://www.upmedia.mg/search.php?sh_keyword=%E5%95%B5%E7%B7%B9'

    headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}

    response = requests.get(url,headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")
    titles = soup.select("#news-list > div > dl > dd > a")
    times = soup.select("#news-list > div > dl > dd > div.time")
    img_urls= soup.select("#news-list > div > dl > dt > a > img")

    contents = dict()
    contents['type'] = 'carousel'
    contents['contents'] = []

    index = 0
    for title,time,img_url in zip(titles,times,img_urls):
        if index < 10:
            bo_title = title.text
            bo_href = title.get("href")
            http = "https://www.upmedia.mg/"
            bo_http = http + bo_href
            bo_time = time.text.replace(" ","").replace("\n","")
            bo_img  = img_url.get("src")
            img_http = "https://www.upmedia.mg/"
            bo_img_http = img_http + bo_img
            # print(bo_title)
            # print(bo_time)
            # print(bo_http)
            # print(bo_img_http)
        
            bubble = {
                        "type": "bubble",
                        "hero": {
                            "type": "image",
                            "url": bo_img_http,
                            "size": "full",
                            "aspectRatio": "20:13",
                            "aspectMode": "cover",
                            "action": {
                            "type": "uri",
                            "uri": bo_http
                            }
                        },
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "text",
                                "text": bo_title,
                                "weight": "bold",
                                "size": "xl",
                                "wrap": True
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
                                "style": "link",
                                "height": "sm",
                                "action": {
                                "type": "uri",
                                "label": "點擊前往",
                                "uri": bo_http
                                }
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [],
                                "margin": "sm"
                            }
                            ],
                            "flex": 0
                        }
                        }
            contents['contents'].append(bubble)
            index+=1
    # print(contents)
    message = FlexSendMessage(alt_text="聯盟戰棋",contents=contents)

    return message

# 3c 科技新報
def news_3c_crawler():

    url = 'https://ccc.technews.tw/'

    headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}

    response = requests.get(url,headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")
    #用select 獲取標籤底下的標籤 格式為 標籤.classname+空格+底下的標籤+空格+底下的標籤
    titles = soup.select("h1.entry-title a")
    img_urls= soup.select("div.img a img")

    contents = dict()
    contents['type'] = 'carousel'
    contents['contents'] = []

    index = 0
    for title,img_url in zip(titles,img_urls):
        if index < 10:
            news3c_title = title.text
            news3c_http = title.get("href")
            news3c_img = img_url.get("src")
            # print(news3c_title)
            # print(news3c_http)
            # print(news3c_img)
        
            bubble = {
                        "type": "bubble",
                        "hero": {
                            "type": "image",
                            "url": news3c_img,
                            "size": "full",
                            "aspectRatio": "20:13",
                            "aspectMode": "cover",
                            "action": {
                            "type": "uri",
                            "uri": news3c_http
                            }
                        },
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "text",
                                "text": news3c_title,
                                "weight": "bold",
                                "size": "xl",
                                "wrap": True
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
                                "style": "link",
                                "height": "sm",
                                "action": {
                                "type": "uri",
                                "label": "點擊前往",
                                "uri": news3c_http
                                }
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [],
                                "margin": "sm"
                            }
                            ],
                            "flex": 0
                        }
                        }
            contents['contents'].append(bubble)
            index+=1
    # print(contents)
    message = FlexSendMessage(alt_text="科技新聞",contents=contents)

    return message

# 18comic
def c18comic_crawler():

    url="https://18comic.vip/user/chri1350j/favorite/albums?o=mp"

    headers = { 'cookie':'__cfduid=d3af1fe4e02395143768f49120192d89a1612161290; _gid=GA1.2.537470263.1612161292; shunt=1; AVS=pgucjspmo4rgafa4vinl3feug4; ipcountry=TW; ipm5=ad96616d894884f20b4e263448a05911; _ga_YYJWNTTJEN=GS1.1.1612339484.9.1.1612339785.59; _gat_ga0=1; _gat_ga1=1; _ga=GA1.2.2093487367.1612161292; _gat_gtag_UA_99252457_3=1; cover=1; _gali=chk_cover',
        'User-Agent':"ua.random"}

    response = requests.get(url,headers = headers)

    soup = BeautifulSoup(response.text, "html.parser")

    titles = soup.findAll("div","video-title title-truncate")
    # 抓出 class 為 thumb-overlay 的 <div>，底下緊接著 標籤為a，底下又接著網址為 /album 開頭的超連結。
    https = soup.select('div.thumb-overlay > a[href^="/album"]')
    jpgs = soup.findAll("img","img-responsive")

    contents = dict()
    contents['type'] = 'carousel'
    contents['contents'] = []
    
    index=0
    for title,http,jpg in zip(titles,https,jpgs):
        if index < 10:
            c18title = title.text
            c18href = http.get("href")
            c18src = jpg.get("src")
            c18http = "https://18comic.vip/"
            c18comic_url= c18http +c18href
            c18jpg_url = c18http + c18src[:-3]
            
            # print(c18title)
            # print(c18comic_url)
            # print(c18jpg_url)

            bubble = {
                        "type": "bubble",
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "image",
                                "url": c18jpg_url,
                                "size": "full",
                                "aspectMode": "cover",
                                "aspectRatio": "2:3",
                                "gravity": "top",
                                "action": {
                                "type": "uri",
                                "label": "action",
                                "uri": c18comic_url
                                }
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                    {
                                        "type": "text",
                                        "text": c18title,
                                        "size": "xl",
                                        "color": "#ffffff",
                                        "weight": "bold"
                                    }
                                    ]
                                }
                                ],
                                "position": "absolute",
                                "offsetBottom": "0px",
                                "offsetStart": "0px",
                                "offsetEnd": "0px",
                                "backgroundColor": "#9D9D9D80",
                                "paddingAll": "20px",
                                "paddingTop": "18px",
                                "action": {
                                "type": "uri",
                                "label": "action",
                                "uri": c18comic_url
                                }
                            }
                            ],
                            "paddingAll": "0px"
                        }
                        }
            contents['contents'].append(bubble)
            index+=1
    # print(contents)
    message = FlexSendMessage(alt_text="18c",contents=contents)

    return message
# c18comic_crawler()