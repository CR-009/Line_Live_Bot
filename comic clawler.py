import requests
from bs4 import BeautifulSoup
import re

url="https://18comic.vip/user/chri1350j/favorite/albums?o=mp"

headers = { 'cookie':'__cfduid=d3af1fe4e02395143768f49120192d89a1612161290; _gid=GA1.2.537470263.1612161292; shunt=1; AVS=pgucjspmo4rgafa4vinl3feug4; ipcountry=TW; ipm5=ad96616d894884f20b4e263448a05911; _ga_YYJWNTTJEN=GS1.1.1612339484.9.1.1612339785.59; _gat_ga0=1; _gat_ga1=1; _ga=GA1.2.2093487367.1612161292; _gat_gtag_UA_99252457_3=1; cover=1; _gali=chk_cover',
    'User-Agent':"ua.random"}

response = requests.get(url,headers = headers)

soup = BeautifulSoup(response.text, "html.parser")
titles = soup.findAll("div","video-title title-truncate")

# 抓出 class 為 thumb-overlay 的 <div>，底下緊接著 標籤為a，底下又接著網址為 /album 開頭的超連結。
https = soup.select('div.thumb-overlay > a[href^="/album"]')

jpgs = soup.findAll("img","img-responsive")




for title,http,jpg in zip(titles,https,jpgs):
     c18title = title.text
     c18href = http.get("href")
     c18src = jpg.get("src")
     c18http = "https://18comic.vip/"
     c18comic_url= c18http +c18href
     c18jpg_url = c18http + c18src[:-3]
     
     print(c18title)
     print(c18comic_url)
     print(c18jpg_url)
