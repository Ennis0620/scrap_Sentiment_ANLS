import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import csv
import time
import re

def get_soup(url):     #對網頁提出要求  剖析網頁
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
    r = requests.get(url, headers = headers)
    soup = BeautifulSoup(r.text, "lxml")
    return soup



hotel_url=[]#紀錄所有飯店的URL 以便後續進去爬取評論資料
next_url="https://www.tripadvisor.com.tw/Hotels-g13806620-Hengchun_Pingtung-Hotels.html" #初始頁面的url 之後會替成下一頁的按鈕
count=0

with open('dataset_Hengchun.csv', 'a+', newline='' ,encoding='utf-8-sig') as csvfile:
               # 建立 CSV 檔寫入器
               writer = csv.writer(csvfile)
               writer.writerow(["飯店名稱","評分","評價"])

s = time.time()


#所有台南飯店url 
while True:
    
    if count==20: break   
    count+=1

    if count%10==0: print("抓取幾筆url:",count)
    
    tripadvisor_tainan = get_soup(next_url)
    #每個飯店名稱
    div = tripadvisor_tainan.find_all("div", attrs = {"class", "listing_title"}) 
    
    for index,i in enumerate(div):
        if index!= 0 : #因為第一筆都是贊助商的飯店 所以不統計
            div_href = i.find("a").get("href")
            #過濾重複的飯店
            if "https://www.tripadvisor.com.tw" + div_href not in hotel_url:
                hotel_url.append("https://www.tripadvisor.com.tw" + div_href)
    
    #找下一頁的class   
    div_button = tripadvisor_tainan.find("div", attrs = {"class", "unified ui_pagination standard_pagination ui_section listFooter"})
    bnt_next = div_button.find("a").get("href")

    next_url = "https://www.tripadvisor.com.tw"+bnt_next



#一一去存下的url爬取評價和評論
for i in hotel_url:
    URL = get_soup(i)
    
    hotel_name = URL.find("h1",attrs={"class","_1mTlpMC3"})
    
    evaluation = URL.find_all("div",attrs = {"class","oETBfkHU"})
    
    #有些飯店沒有評論 因此會是空的  如果是空的就跳過
    if len(evaluation) == 0 : continue
    
    #評論也分成好幾頁 要點下一個按鈕一直找到最後
    
    print("--------------",hotel_name.text,"-------------")
    
    c = 0
    check=True
    
    while check:
        
        for index,j in enumerate(evaluation):
            c+=1
            if c%100==0 : print(c)
            #評論
            e = j.find("q",attrs={"class","IRsGHoPm"})
            #評分 因為該評分是用圖案顯示 只好抓取標籤的class文字 進行評分的轉換
            e_rate = j.find("span",attrs={"class","ui_bubble_rating"})
            s_rate= str(e_rate)
            s_rate = s_rate.split("_")[3][0]
            
            with open('dataset_Hengchun.csv', 'a+', newline='' ,encoding='utf-8-sig') as csvfile:
               # 建立 CSV 檔寫入器
               writer = csv.writer(csvfile)
               writer.writerow([str(hotel_name.text),s_rate,str(e.text)])
               
            #print(s_rate)
            #print(c,"-----",e.text)
                                   
            #一頁只有5筆 因此之後要去找url
            if index == len(evaluation)-1:
                
                #如果下一頁無法按下 代表已經沒評論了
                if  URL.find("span",attrs={"class","ui_button nav next primary disabled"}) is not None:
                    check = False
                    break
                #否則代表還可以繼續按下一頁
                else:
                    pg = URL.find("span",attrs={"class","mxlinKbW"})
                    #因為他數字的形式都是(1,000)之類的 所以要去掉不必要符號
                    pg = int(re.sub(r'[^\w\s]', "",str(pg.text)))
                    
                    if  pg <= 5:
                        #代表只有一頁
                        check = False
                        break
                    #找到下一頁的連結
                    else:
                        nxt_eva = URL.find("a",attrs={"class","ui_button nav next primary"}).get("href")                   
                        URL = "https://www.tripadvisor.com.tw" + nxt_eva                     
                        #前往下一頁
                        URL = get_soup(URL)
                        #抓取所有評論區塊
                        evaluation = URL.find_all("div",attrs = {"class","oETBfkHU"})               
                
e = time.time()

print("耗時:",round(e-s,6))            
