import requests as req
import re
import bs4

def movie_crawler():

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

    contentmv=""
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
            Movie_name = tcount + ". "+ "【"+ title.a.string.replace(" ","").replace("\n","")+"】"
            Movie_ID = "電影ID: " + movie_id
            Screening = time.text.replace(" ","").replace("\n","")
            Expect_score = "期待度: "  + expect.text
            Like_score = "綜合評分: " + like['data-num'] + " 分"
            Movie_Http = "影片網址: " + href
            contentmv += "{}\n{}\n{}\n{}\n{}\n{}\n\n".format(Movie_name,Movie_ID,Screening,Expect_score,Like_score,Movie_Http)
            print(contentmv)
    return contentmv
