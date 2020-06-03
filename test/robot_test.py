from ..app.db import InsertTblNews
from app.robots import news_from_tejaratnews



def tejerat_test():
    tejarat = news_from_tejaratnews()
    data = tejarat.getData()
    return InsertTblNews(data)

if __name__ == "__main__":
    print(tejerat_test())
