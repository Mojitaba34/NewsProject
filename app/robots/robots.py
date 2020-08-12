
from selenium import webdriver   # for webdriver
from selenium.webdriver.support.ui import WebDriverWait  # for implicit and explict waits
from selenium.webdriver.chrome.options import Options  # for suppressing the browser

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


import time
import requests
from app.admin import config
import lxml.html as html
from app.admin import db
import json



class PageContent():
    '''
    This is a Class for read Page Html Content for access Page with Xpath to extaract data with it 
    Here we have a Staticmethod
    This function have url argument and with request object we can get page Html content and decode 
    And Finaly returns a Html content
    '''

    def main(self,url):
       PATH = r"C:\Program Files (x86)/chromedriver.exe"
       self.option = webdriver.ChromeOptions()
       self.option.add_argument('headless')
       self.driver = webdriver.Chrome(PATH,options=self.option)
       self.driver.get(url)
       return self.driver.page_source


   #  def images_data(self,url):
   #     PATH = r"C:\Program Files (x86)\chromedriver.exe"
   #     self.option = webdriver.ChromeOptions()
   #     self.option.add_argument('headless')
   #     self.driver = webdriver.Chrome(PATH,options=self.option)
   #     self.driver.get(url)
   #     try:
   #       self.element = WebDriverWait(self.driver, 20).until(
   #          EC.presence_of_element_located((By.CLASS_NAME, "media-object wp-post-image lazy-loaded"))
   #       )
   #       return self.element
   #      #  articals = self.element.find_element_by_class_name("news-media media news-media__row news-media__l")
   #      #  for artical in articals:
   #      #     image_link = artical.find_element_by_class_name("media-object wp-post-image lazy-loaded")
   #      #     if "jpg" in str(image_link.src):
   #      #         print(image_link.src)
   #     finally:
   #        self.driver.quit()

      

class news_from_tejaratnews():
    '''
    Class for tejaratNews 

    we have a page link and pass it to staticmethod to return url link content 
    After we got content we can access to tags with xpath 

    Xpath returns a list object with the news content such as Title, News link, And Body of news 

    '''
    def __init__(self):
      url = "https://tejaratnews.com/category/%d8%a7%d9%82%d8%aa%d8%b5%d8%a7%d8%af-%d8%ac%d9%87%d8%a7%d9%86"
      self.content = PageContent()
      self.response = self.content.main(url)
    #   self.images_data = html.fromstring(self.content.images_data(url))
      self.root = html.fromstring(self.response)


    '''
    img_lnk this function gets a news image with Xpath 

    Xpath returns a list of image links in the site 

    '''
    def img_lnk(self):
        news_image_dec = []
        news_image_dec =self.root.xpath("//article[contains(@class, 'news-media media news-media__row news-media__l')]//div[contains(@class, 'news-media__image media-left')]//img/@data-src")
        return news_image_dec
    
    '''
    news_title returns news Titles with Xpath 

    Xpath returns a list of Titles in the site 
    
    '''

    def news_title(self):
        title_lst = []
        title_lst = self.root.xpath("//article[contains(@class, 'news-media media news-media__row news-media__l')]//div[contains(@class, 'news-media__title')]//a/text()")
        return title_lst

    '''
    new_content returns contents of news with Xpath 

    Xpath returns a list of new_content in the site 
    
    '''

    def news_content(self):
        content_list = []
        content_list = self.root.xpath("//article[contains(@class, 'news-media media news-media__row news-media__l')]//p[contains(@class, 'news-media__description hidden-xs')]/text()")
        return content_list

    '''
    news_link returns news Link with Xpath 

    Xpath returns a list of news links in the site 
    
    '''

    def news_link(self):
        link_news = []
        link_news = self.root.xpath("//article[contains(@class, 'news-media media news-media__row news-media__l')]//div[contains(@class, 'news-media__title')]//a/@href")
        return link_news

    '''
    returning a dictionary data for store in dataBase

    '''
    def getData(self):
        data= {
            'news_image_link': self.img_lnk(),
            'news_title': self.news_title(),
            'news_content': self.news_content(),
            'news_link':self.news_link()
        }
        posts=[]
        data_len = self.news_title()
        for post in range(len(data_len)):
            posts.append({"news_img_link":data['news_image_link'][post],"title":data['news_title'][post],"content":data['news_content'][post],"link":data['news_link'][post]})
        return posts#TODO: InsertTblNews()
        



class news_from_tasnimnews():

    '''
    Class for tasnimnews 

    we have a page link and pass it to staticmethod to return url link content 
    After we got content we can access to tags with xpath 

    Xpath returns a list object with the news content such as Title, News link, And Body of news 

    '''


    '''
    
    Url for news section on tasnimnews 
    root is the return value of the staticmethod in PageContent
    
    '''

    def __init__(self):
      url = "https://www.tasnimnews.com/fa/service/85/%D8%A7%D9%82%D8%AA%D8%B5%D8%A7%D8%AF-%D8%AC%D9%87%D8%A7%D9%86"
      self.content = PageContent()
      self.response = self.content.main(url)
      self.root = html.fromstring(self.response)


    '''
    img_lnk this function gets a news image with Xpath 

    Xpath returns a list of image links in the site 

    '''

    def img_lnk(self):
        news_image_dec = []
        news_image_dec =self.root.xpath("//article[contains(@class, 'list-item')]//div[contains(@class,'col-md-4 col-xs-4 image-container vcenter')]//img/@src")
        return news_image_dec


    '''
    news_title returns news Titles with Xpath 

    Xpath returns a list of Titles in the site 
    
    '''

    def news_title(self):
        title_lst = []
        title_lst = self.root.xpath("//article[contains(@class, 'list-item')]//div[contains(@class,'col-md-8 col-xs-8 text-container vcenter')]//h2[contains(@class,'title')]/text()")
        return title_lst

    '''
    new_content returns contents of news with Xpath 

    Xpath returns a list of new_content in the site 
    
    '''

    def news_content(self):
        content_list = []
        content_list = self.root.xpath("//article[contains(@class, 'list-item')]//div[contains(@class,'col-md-8 col-xs-8 text-container vcenter')]//h4[contains(@class,'lead')]/text()")
        return content_list

    '''
    news_link returns news Link with Xpath 

    Xpath returns a list of news links in the site 

    Because of Xpath returns a Incomplete link we need to add it with link_add string to links work properly

    '''

    def news_link(self):
        link_news = []
        link_news = self.root.xpath("//article[contains(@class, 'list-item')]/a/@href")
        modified_link = []
        link_add = "https://www.tasnimnews.com"
        for lnk in link_news:
            modified_link.append(str(link_add)+ str(lnk))
        
        return modified_link

    '''
    returning a dictionary data for store in dataBase

    '''
    def getData(self):
        data= {
            'news_image_link': self.img_lnk(),
            'news_title': self.news_title(),
            'news_content': self.news_content(),
            'news_link':self.news_link()
        }
        posts=[]
        for post in range(len(self.news_title())):
            posts.append({"news_img_link":data['news_image_link'][post],"title":data['news_title'][post],"content":data['news_content'][post],"link":data['news_link'][post]})
        return posts#TODO: InsertTblNews()



class news_from_arzdigital():

    '''
    Class for arzdigital 

    we have a page link and pass it to staticmethod to return url link content 
    After we got content we can access to tags with xpath 

    Xpath returns a list object with the news content such as Title, News link, And Body of news 

    '''

    '''

    Url for news section on arzdigital 
    root is the return value of the staticmethod in PageContent
    
    '''
    def __init__(self):
      url = "https://arzdigital.com/category/news/world-news/"
      self.content = PageContent()
      self.response = self.content.main(url)
      self.root = html.fromstring(self.response)



    '''

    img_lnk this function gets a news image with Xpath 

    Xpath returns a list of image links in the site 

    '''
    def img_lnk(self):
        news_image_dec = []
        news_image_dec =self.root.xpath("//div[contains(@class, 'arz-col arz-col-md arz-last-post-image')]/img/@src")
        return news_image_dec

    '''
    news_title returns news Titles with Xpath 

    Xpath returns a list of Titles in the site 
    
    '''
    def news_title(self):
        title_lst = []
        title_lst = self.root.xpath("//div[contains(@class, 'arz-row-sb arz-posts')]//h3[contains(@class,'arz-last-post-title')]/text()")
        return title_lst

    '''
    new_content returns contents of news with Xpath 

    Xpath returns a list of new_content in the site 
    
    '''

    def news_content(self):
        content_list = []
        content_list = self.root.xpath("//div[contains(@class, 'arz-row-sb arz-posts')]//div[contains(@class,'arz-last-post-text')]/p/text()")
        return content_list

    '''
    news_link returns news Link with Xpath 

    Xpath returns a list of news links in the site 
    
    '''

    def news_link(self):
        link_news = []
        link_news = self.root.xpath("//div[contains(@class, 'arz-row-sb arz-posts')]/a/@href")
        return link_news

    '''
    returning a dictionary data for store in dataBase

    '''
    def getData(self):
        data= {
            'news_image_link': self.img_lnk(),
            'news_title': self.news_title(),
            'news_content': self.news_content(),
            'news_link':self.news_link()
        }
        posts=[]
        for post in range(len(self.news_title())):
            posts.append({"news_img_link":data['news_image_link'][post],"title":data['news_title'][post],"content":data['news_content'][post],"link":data['news_link'][post]})
        return posts #TODO: InsertTblNews()




class news_from_mehrnews():

    def __init__(self):
      url = "https://www.mehrnews.com/tag/%D9%88%DB%8C%D8%B1%D9%88%D8%B3+%DA%A9%D8%B1%D9%88%D9%86%D8%A7"
      self.news_link_url = "https://www.mehrnews.com"
      self.content = PageContent()
      self.response = self.content.main(url)
      self.root = html.fromstring(self.response)

    def image_links(self):
        img_links = []
        img_links = self.root.xpath("//section[contains(@class,'box list list-bordered list-thumbs thumbs-lg highlights no-header  _types')]/div/ul//li//img/@src")
        return img_links

    def news_title(self):
        news_title = []
        news_title = self.root.xpath("//section[contains(@class,'box list list-bordered list-thumbs thumbs-lg highlights no-header  _types')]/div/ul//li//h3/a/text()")
        return news_title

    def news_content(self):
        news_contenct = []
        news_contenct = self.root.xpath("//section[contains(@class,'box list list-bordered list-thumbs thumbs-lg highlights no-header  _types')]/div/ul//li//p/text()")
        return news_contenct

    def news_link(self):
        news_link = []
        news_link = self.root.xpath("//section[contains(@class,'box list list-bordered list-thumbs thumbs-lg highlights no-header  _types')]/div/ul//li//h3/a/@href")
        modified_link = []
        for lnk in news_link:
            modified_link.append(str(self.news_link_url)+ str(lnk))
        return modified_link



    '''
    returning a dictionary data for store in dataBase

    '''
    def getData(self):
        data= {
            'news_image_link': self.image_links(),
            'news_title': self.news_title(),
            'news_content': self.news_content(),
            'news_link':self.news_link()
        }
        posts=[]
        for post in range(len(self.news_title())):
            posts.append({"news_img_link":data['news_image_link'][post],"title":data['news_title'][post],"content":data['news_content'][post],"link":data['news_link'][post]})
        return posts #TODO: InsertTblNews()


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


