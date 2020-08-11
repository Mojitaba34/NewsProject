from app.admin import db as db_admin
from app.robots import robots
import time
import threading




class robot_runner:

    timer_tejarat      = 0
    timer_tasnim       = 0
    timer_arzdigital   = 0
    state_tejarat      = 0
    state_tasnim       = 0
    state_arzdigital   = 0
    


    def refresh_data(self):
        while True:
            robotStates = db_admin.get_robots()
            self.timer_tejarat      = robotStates[0][2]
            self.timer_tasnim       = robotStates[1][2]
            self.timer_arzdigital   = robotStates[2][2]
            self.state_tejarat      = robotStates[0][1]
            self.state_tasnim       = robotStates[1][1]
            self.state_arzdigital   = robotStates[2][1]
            time.sleep(2)


    def tejarat_Robot(self):
        while True:            
            if self.state_tejarat == 0:
                tejarat_news = robots.news_from_tejaratnews()
                data = tejarat_news.getData()
                print("--------------Tejarat----------------")
                print("tejarat=  "+db.InsertTblNews(data))
                print("timer=  "+str(self.timer_tejarat))
                print("state= "+str(self.state_tejarat))
                print("------------------------------")
                time.sleep(self.timer_tejarat)



    def tasnim_Robot(self):
        while True:
            if self.state_tasnim == 0:
                tasnim_news = robots.news_from_tasnimnews()
                data = tasnim_news.getData()
                print("--------------Tasnim----------------")
                print("tasnim=  "+db.InsertTblNews(data))
                print("timer=  "+str(self.timer_tasnim))
                print("state= "+str(self.state_tasnim))
                print("------------------------------")
                time.sleep(self.timer_tasnim)


    def arzdigital_Robot(self):
        while True:
                if self.state_arzdigital == 0:
                    arzdigital_news = robots.news_from_arzdigital()
                    data = arzdigital_news.getData()
                    print("--------------Arzdigital----------------")
                    print("arzdigital=  "+db.InsertTblNews(data))
                    print("timer=  "+str(self.timer_arzdigital))
                    print("state= "+str(self.state_arzdigital))
                    print("------------------------------")
                    time.sleep(self.timer_arzdigital)


    def threadRun(self):
        while True:
            if self.state_tasnim == 1:
                p1 = threading.Thread(target=self.tejarat_Robot)
                p2 = threading.Thread(target=self.tasnim_Robot)
                p3 = threading.Thread(target=self.arzdigital_Robot)
                p4 = threading.Thread(target=self.refresh_data)
                """
                Started threads by start() method
                """
                p1.start()
                p2.start()
                p3.start()
                p4.start()


