import requests
from bs4 import BeautifulSoup
import re

url = 'https://www.upmedia.mg/search.php?sh_keyword=%E5%95%B5%E7%B7%B9'

headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}

response = requests.get(url,headers=headers)

soup = BeautifulSoup(response.text, "html.parser")
titles = soup.select("#news-list > div > dl > dd > a")
times = soup.select("#news-list > div > dl > dd > div.time")
img_urls= soup.select("#news-list > div > dl > dt > a > img")


for title,time,img_url in zip(titles,times,img_urls):
    bo_title = title.text
    bo_href = title.get("href")
    http = "https://www.upmedia.mg/"
    bo_http = http + bo_href
    bo_time = time.text.replace(" ","").replace("\n","")
    bo_img  = img_url.get("src")
    img_http = "https://www.upmedia.mg/"
    bo_img_http = img_http + bo_img
    print(bo_title)
    print(bo_time)
    print(bo_http)
    print(bo_img_http)

    