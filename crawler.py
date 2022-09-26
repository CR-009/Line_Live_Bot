import requests
from bs4 import BeautifulSoup


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
            print(contentfn)
        else:
            break
        
    return contentfn


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

def sex_crawler():
    
    url="https://www.ptt.cc/bbs/sex/index.html"
    my_headers = {'cookie':'over18=1'}
    response = requests.get(url,headers=my_headers)
    soup = BeautifulSoup(response.text, "html.parser")
    sex_titles = soup.find_all('div','title')
   
    contentsex = ""

    for index_sex, sex_title in enumerate(sex_titles):
        if index_sex < 10:
            title = sex_title.text
            sex_href  = sex_title.select_one("a").get("href")
            sex_http = "https://www.ptt.cc/"
            contentsex += "{}\n{}\n".format(title,sex_http + sex_href)
        else:
            break
        
    return contentsex
