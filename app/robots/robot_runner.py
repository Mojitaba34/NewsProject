from app import db
from app.robots import robots
def tejarat_test():
    tejarat_news = robots.news_from_tejaratnews()
    data = tejarat_news.getData()
    print(db.InsertTblNews(data))

def tasnim_test():
    tasnim_news = robots.news_from_tasnimnews()
    data = tasnim_news.getData()
    print(db.InsertTblNews(data))

def arzdigital_test():
    arzdigital_news = robots.news_from_arzdigital()
    data = arzdigital_news.getData()
    print(db.InsertTblNews(data))


"""if __name__ == "__main__":
    while True:
        if db.getStateTejaratNews() == 0:
            pass # tejaratNews Runned
        elif db.getStateTasnim() == 0:
            pass # Tasnim Runned
        elif db.getStateArzdigital() == 0:
            pass # Arzdigital Runned"""