import json
import datetime
import feedparser
import os

urlBase1 = "https://www.nhk.or.jp/rss/news/cat"
urlBase2 = "https://www3.nhk.or.jp/lnews/"

# 取得してまずdictにする
newsDict = []
for i in range(8):
    url = urlBase1 + str(i) + ".xml"
    raw = feedparser.parse(url)

    # ジャンルごとのニュース
    newsList = {}
    newsList['cat'] = raw['feed']['title']
    newsList['updated'] = raw['feed']['updated']
    news = []
    for rawArticle in raw['entries']:
        article = {}
        article['title'] = rawArticle['title']
        article['summary'] = rawArticle['summary']
        article['published'] = rawArticle['published']
        article['link'] = rawArticle['link']
        news.append(article)
    newsList['news'] = news
    newsDict.append(newsList)

#地域ごとのニュースも取れるみたいなのでいれておく
#県庁所在地(東京はshutoken, 那覇はokinawaっぽい)
kencho = ["sapporo","aomori","morioka","sendai","akita","yamagata","fukushima",
          "mito","utsunomiya","maebashi","saitama","chiba","shutoken","yokohama",
          "niigata","toyama","kanazawa","fukui","kofu","nagano","gifu","shizuoka","nagoya",
          "tsu","otsu","kyoto","osaka","kobe","nara","wakayama",
          "tottori","matsue","okayama","hiroshima","yamaguchi","tokushima","takamatsu","matsuyama","kochi",
          "fukuoka","saga","nagasaki","kumamoto","oita","miyazaki","kagoshima","okinawa"]

#47都道府県分
for ken in kencho:
    url = urlBase2 + ken + "/toplist.xml"
    raw = feedparser.parse(url)

    #県ごとのニュース
    newsList = {}
    newsList['cat'] = ken
    newsList['updated'] = raw['feed']['updated']
    news = []
    for rawArticle in raw['entries']:
        article = {}
        article['title'] = rawArticle['title']
        article['summary'] = rawArticle['summary']
        article['published'] = rawArticle['published']
        article['link'] = rawArticle['link']
        news.append(article)
    newsList['news'] = news
    newsDict.append(newsList)

# jsonに変換
newsJson = json.dumps(newsDict, ensure_ascii=False)

# ファイル出力
sourcePath = os.path.dirname(__file__)
f = open(sourcePath+"/news.json", "w", encoding='utf-8')
f.write(newsJson)
f.close()
f = open(sourcePath+"/date.json", "w",encoding='utf-8')

dateDict={}
dateDict['committed']=str(datetime.datetime.now())
dateDictJson = json.dumps(dateDict,ensure_ascii=False)
f.write(dateDictJson)
f.close()
