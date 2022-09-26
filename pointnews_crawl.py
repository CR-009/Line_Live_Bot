import requests
import selenium
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import short_url

def pointnews_crawler():

    url = "https://tw.yahoo.com/"
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}

    list_req = requests.get(url,headers=headers)
    soup = BeautifulSoup(list_req.content, "html.parser")

    news_list = soup.find_all('a',{"class":"Fz(16px) LineClamp(1,20px) Fw(700) Td(n) Td(u):h C(#324fe1) V(h) active_V(v)"})

    content = ""

    for index, d in enumerate(news_list):
        if index <8:
            title = d.text
            href  = d.get("href")
            content += "{}\n{}\n".format(title, href)
        else:
            break
        
    return content

pointnews_crawler()


    

