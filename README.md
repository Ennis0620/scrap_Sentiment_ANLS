Tripadvisor飯店評論、評價正負面分析
===

# Introduction

# Detail
### 資料前處理:
分別爬取台北、台中、台南的飯店評論，統計各評價數量，因為只分成正負評，所以將評分為4、5星列為正評(=1),1、2、3星列為負評(=0)。

</br>

採用下採樣(Undersampling)，從正評當中隨機選取(不重複)和負評一樣的數量。

</br>

接著對每一筆評論做斷詞處理，使用sklearn的CountVectorizer計算詞出現頻率並過濾停用詞、稀有的詞彙。

### 選擇模型
MultinomialNB、SVM訓練


# Demo
北、中、南評論總計

![](https://i.imgur.com/8Iyh3Cj.png)
![](https://i.imgur.com/wpDYnL9.png)

下採樣後數量

![](https://i.imgur.com/b7mpmZc.png)

去除稀有詞彙且過濾停用詞轉成向量

![](https://i.imgur.com/pVQnmqc.png)

MultinomialNB 結果有84%準確率

![](https://i.imgur.com/Nk7XFeO.png)

SVM訓練 c=0.05(容錯率變高，泛化效果較好) 結果有85%準確率

![](https://i.imgur.com/wEubH9i.png)



# Requirement
     Jupyter Notebook

# Package
    code
        │  dataset_Taichung.csv          台中評論
        │  dataset_Tainan_test.csv       台南評論
        │  dataset_Taipei.csv            台北評論
        │  lexicon_dict.txt              常用字辭典
        │  mask_alice.png                文字雲形狀          
        │  SourceHanSansTW-Regular.otf   中文字型
        │  stopword.txt                  停用詞
        │  wc.jpg                        文字雲結果(正面)
        │  wc2.jpg                       文字雲結果(負面) 
        │  ML.ipynb                      主要程式碼
        │  
        └─web_scraping
                scraping.py              爬蟲程式
# Problems
1.如何解決資料及不平衡問題

2.怎麼計算文字正負面情緒
# Solve
1.根據手上資料數量多寡，若資料量夠多就用下採樣，否則就使用上採樣

2.將文字像量化後透過機器學習的方式找出所屬類別