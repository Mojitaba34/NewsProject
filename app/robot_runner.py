import db

import robots

tejarat_news = robots.news_from_tejaratnews()
data = tejarat_news.getData()
print(db.InsertTblNews(data))