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
    newsList['newsList'] = news
    newsDict.append(newsList)

# 地域ごとのニュースも取れるみたいなのでいれておく
# 県庁所在地(東京はshutoken, 那覇はokinawaっぽい)
kencho = ["sapporo", "aomori", "morioka", "sendai", "akita", "yamagata", "fukushima",
          "mito", "utsunomiya", "maebashi", "saitama", "chiba", "shutoken", "yokohama",
          "niigata", "toyama", "kanazawa", "fukui", "kofu", "nagano", "gifu", "shizuoka", "nagoya",
          "tsu", "otsu", "kyoto", "osaka", "kobe", "nara", "wakayama",
          "tottori", "matsue", "okayama", "hiroshima", "yamaguchi", "tokushima", "takamatsu", "matsuyama", "kochi",
          "fukuoka", "saga", "nagasaki", "kumamoto", "oita", "miyazaki", "kagoshima", "okinawa"]

todofuken = ["北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県",
             "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県",
             "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県", "静岡県", "愛知県",
             "三重県", "滋賀県", "京都府", "大阪府", "兵庫県", "奈良県", "和歌山県",
             "鳥取県", "島根県", "岡山県", "広島県", "山口県", "徳島県", "香川県", "愛媛県", "高知県",
             "福岡県", "佐賀県", "長崎県", "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"]

# 47都道府県分
for i, ken in enumerate(kencho):
    url = urlBase2 + ken + "/toplist.xml"
    raw = feedparser.parse(url)
    # 県ごとのニュース
    newsList = {}
    newsList['cat'] = todofuken[i]
    newsList['updated'] = raw['feed']['updated']
    news = []
    for rawArticle in raw['entries']:
        article = {}
        article['title'] = rawArticle['title']
        article['summary'] = rawArticle['summary']
        article['published'] = rawArticle['published']
        article['link'] = rawArticle['link']
        news.append(article)
    newsList['newsList'] = news
    newsDict.append(newsList)

# jsonに変換
newsJson = json.dumps(newsDict, ensure_ascii=False)

# ファイル出力
sourcePath = os.path.dirname(__file__)
f = open(sourcePath+"/news.json", "w", encoding='utf-8')
f.write(newsJson)
f.close()
f = open(sourcePath+"/date.json", "w", encoding='utf-8')

dateDict = {}
dateDict['committed'] = str(datetime.datetime.now())
dateDictJson = json.dumps(dateDict, ensure_ascii=False)
f.write(dateDictJson)
f.close()
