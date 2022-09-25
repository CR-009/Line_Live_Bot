import requests as req
import re
import bs4
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#取得網頁資訊

url_movie_info = "https://movies.yahoo.com.tw/movie_intheaters.html"

response = req.get(url_movie_info)
response.encoding = 'utf-8'
#print(response.text)

#解析原始碼,取得每篇文章的標題

# 將 data 也就是 HTML 資料定義到 BeautifulSoup 物件內，並用 html.parser 解析 HTML 內容
soup = bs4.BeautifulSoup(response.text,"lxml")
# print(soup)

# 電影標題
titles = soup.findAll("div",'release_movie_name')
#上映日期
release_time = soup.find_all("div",class_="release_movie_time")
#期待度
expect_percents = soup.select("dt div span")
# 綜合評分
likes_score = soup.find_all("span",attrs={'data-num':re.compile('.*')})
#影片網址
srcs = soup.find_all(class_="btn_s_introduction")

print(" ")
print("   電影資訊-上映中")
print(" ")

#用zip函數 合併 titles,likes_score,expect_percents for迴圈
count=0
for title,like,expect,time,src in zip(titles,likes_score,expect_percents,release_time,srcs) : 
    # 如果標題包含 a 標籤(沒有被刪除),印出來
    if title.a != None:
        count+=1
        #計算第幾個
        tcount=str(count) 
        #取得電影網址
        href= src.get('href')
        # 電影ID
        movie_id = href[-5:]
        print(tcount + ". "+ "【"+ title.a.string.replace(" ","").replace("\n","")+"】")
        print("======================================")
        print("電影ID: " + movie_id)
        print(time.text.replace(" ","").replace("\n",""))
        print("期待度: "  + expect.text)
        print("綜合評分: " + like['data-num'] + " 分")
        print("影片網址: " + href)
        print("-----------------------------------------")
        
        url = "https://movies.yahoo.com.tw/movietime_result.html/id=" + movie_id

        #selenium 載入
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications" : 2}
        chrome_options.add_experimental_option("prefs",prefs)

        # 以下三個註解打開，瀏覽器就不會開啟
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        # 禁用LOG檔
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        #開啟瀏覽器
        driver = webdriver.Chrome(options=chrome_options)

        driver.get(url)
        
        # 等待時刻表出現
        element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="content_l"]/div/div/div[2]/div[1]/ul/li[1]/label'))
            )

        #台北市場次
        TPtheaters_time = driver.find_element_by_xpath('//*[@id="content_l"]/div/div/div[2]/div[1]/div[3]/div/div[1]')
        print(TPtheaters_time.text)
        print("-----------------------------------------")
        #新北市場次
        NTPtheaters_time = driver.find_element_by_xpath('//*[@id="content_l"]/div/div/div[2]/div[1]/div[3]/div/div[2]')
        print(NTPtheaters_time.text)
        print("-----------------------------------------")
        print("======================================")
        print(" ")
        driver.quit()


# count=0
# for src  in srcs:
#     src_href = src.get('href')
#     movie_id = src_href[-5:]
#     #selenium 載入
#     chrome_options = webdriver.ChromeOptions()
#     prefs = {"profile.default_content_setting_values.notifications" : 2}
#     chrome_options.add_experimental_option("prefs",prefs)

#     # 以下三個註解打開，瀏覽器就不會開啟
#     chrome_options.add_argument('--headless')
#     chrome_options.add_argument('--no-sandbox')
#     chrome_options.add_argument('--disable-dev-shm-usage')

#     # 禁用LOG檔
#     chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
#     driver = webdriver.Chrome(options=chrome_options)
#     url = "https://movies.yahoo.com.tw/movietime_result.html/id=" + movie_id
#     driver_s= driver.get(url)
#     time.sleep(2)
#     TPtheaters_time = driver.find_element_by_xpath('//*[@id="content_l"]/div/div/div[2]/div[1]/div[3]/div/div[1]')
#     print(TPtheaters_time.text)
#     print("-----------------------------------------")
#     NTPtheaters_time = driver.find_element_by_xpath('//*[@id="content_l"]/div/div/div[2]/div[1]/div[3]/div/div[2]')
#     print(NTPtheaters_time.text)
#     print("-----------------------------------------")
#     driver.quit()
