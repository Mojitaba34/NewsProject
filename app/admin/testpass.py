import db

news_data = db.get_NewsData()
print(news_data[0]["news_title"])