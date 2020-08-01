import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEnginePage
import bs4 as bs
import urllib.request
from app import db
from pprint import pprint


"""
This class uses for our robot to behave like client that uses browser and get All data from Site

"""
class Client(QWebEnginePage):

   def __init__(self, url):
      self.app = QApplication(sys.argv)
      QWebEnginePage.__init__(self)
      self.loadFinished.connect(self.on_page_load)
      self.load(QUrl(url))
      self.app.exec_()

   def on_page_load(self):
      self.html = self.toHtml(self.Callable)

   def Callable(self, html_str):
      self.html = html_str
      self.app.quit()




class news_from_tejaratnews():

   def __init__(self):
      url = "https://tejaratnews.com/category/%d8%a7%d9%82%d8%aa%d8%b5%d8%a7%d8%af-%d8%ac%d9%87%d8%a7%d9%86"
      self.response = Client(url)

   def tejart(self):

      soup = bs.BeautifulSoup(self.response.html,'html.parser')

      for artical_html in soup.find_all(class_="news-media media news-media__row news-media__l"):
         image_link = artical_html.find('img', class_="media-object wp-post-image")['src']
         title = artical_html.find('figure').a['title']
         description = artical_html.find('p',class_="news-media__description").text
         link = artical_html.find('figure').a['href']
         
         data = { 'img_link':image_link, 
                  'title':title,
                  'desc':description,
                  'link':link}

         db.InsertTblNews(data)
         print("-------------------------------------------------------")# You CAN REMOVE THIS




class news_from_tasnimnews():

   def __init__(self):
      url = "https://www.tasnimnews.com/fa/service/85/%D8%A7%D9%82%D8%AA%D8%B5%D8%A7%D8%AF-%D8%AC%D9%87%D8%A7%D9%86"
      self.fix_url = "https://www.tasnimnews.com"
      self.response = Client(url)
      file = open('./htmltest.html','w')
      file.write(self.response.html)
      file.close()
      self.list_data = []

   def tasnim(self):
      print("This meethod Started!!!!")
      soup = bs.BeautifulSoup(self.response.html,'html.parser')
      for artical in soup.find_all(class_="list-item"):
         image_link = artical.find('img')['src']
         title = artical.find('h2', class_="title").text
         print(title)
         descripton = artical.find('h4', class_="lead").text
         link = artical.find('a')['href']
         link = self.fix_url + link
         self.list_data.append(title)
         """data = { 'img_link':image_link,
                  'title':title,
                  'desc':description,
                  'link':link}
         self.list_data.append(data)"""
      return self.list_data

class news_from_arzdigital():

   def __init__(self):
      url = "https://arzdigital.com/category/news/world-news/"
      self.response = Client(url)
      
   def arzdigi(self):
      
      soup = bs.BeautifulSoup(self.response.html,'html.parser')

      for artical in soup.find_all(class_="arz-last-post arz-row"):
         image_link = artical.find('div',class_="arz-col arz-col-md arz-last-post-image").img['src']
         title = artical.find('h3',class_="arz-last-post-title").text
         link = artical['href']
         data = { 'img_link':image_link, 
                  'title':title,
                  'desc':'',
                  'link':link}

         db.InsertTblNews(data)
         
         print("------------------------------------------------")# You CAN REMOVE THIS

class crypto():
    
    def __init__(self):
        self.CoinList = ['BTCUSDT','ETHUSDT','XRPUSDT','BCHUSDT','LTCUSDT','BNBUSDT','LINKUSDT']
        # https://api.binance.com/api/v3/ticker/price?symbol=ZENBTC
        #API = 'https://api.binance.com/api/v3/ticker/price?symbol={}'

    def get_data(self):
        dict_data = {}
        for coin in self.CoinList:
            r = requests.get(f'https://api.binance.com/api/v3/ticker/price?symbol={coin}')
            data = json.loads(r.text)
            dict_data.__setitem__(data['symbol'],round(float(data["price"]),2))
        return dict_data