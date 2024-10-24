import json
import feedparser
import os

urlBase = "https://www.nhk.or.jp/rss/news/cat"

# 取得してまずdictにする
newsDict = []
for i in range(8):
    url = urlBase + str(i) + ".xml"
    raw = feedparser.parse(url)

    # ジャンルごとのニュース
    newsList = {}
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

# jsonに変換
newsJson = json.dumps(newsList, ensure_ascii=False)

# ファイル出力
sourcePath = os.path.dirname(__file__)
f = open(sourcePath+"/news.json", "w", encoding='utf-8')
f.write(newsJson)
f.close()
