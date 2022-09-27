import requests
from bs4 import BeautifulSoup

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
            break
        
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

    contentHOT = ""

    for index,Htitle in enumerate(titles):
        if index < 10:
            if Htitle.a != None:
                title = Htitle.text
                PTT_href  = Htitle.select_one("a").get("href")
                PTT_http = "https://disp.cc/b/"
                contentHOT += "{}\n{}\n\n".format(title,PTT_http + PTT_href)
                # print(contentHOT)
        
    return contentHOT

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
        else:
            break      
        
    return contentGossiping

#PTT-西斯板
def PTT_Sex_crawler():
    
    url="https://www.ptt.cc/bbs/Sex/index.html"
    my_headers = {'cookie':'over18=1'}
    response = requests.get(url,headers=my_headers)
    soup = BeautifulSoup(response.text, "html.parser")
    titles = soup.find_all('div','title')
    
    contentSex = ""
   
    for index,Stitle in enumerate(titles):
        if index < 7:
            if Stitle.a != None:
                title = Stitle.text
                PTT_href  = Stitle.select_one("a").get("href")
                PTT_http = "https://www.ptt.cc/"
                contentSex += "{}\n{}\n".format(title,PTT_http + PTT_href)
                # print(contentSex)
                
        else:
            break
 
    return contentSex


