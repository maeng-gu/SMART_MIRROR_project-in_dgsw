import pygame, datetime, time, math, sys
import pygame.locals
import requests, json, io, threading
import Module
import MealInfo, ClassInfo, EventInfo, Weather, Show, Naver

data = io.open(sys.path[0] + '/config.json', mode='r', encoding='utf-8').read()
conf = json.loads(data)

mod_mealinfo = MealInfo.MealInfo(
    conf['Open-NEIS-API']['KEY'],
    conf['Open-NEIS-API']['SD_SCHUL_CODE'],
    conf['Open-NEIS-API']['ATPT_OFCDC_SC_CODE']
)
mod_classinfo = ClassInfo.ClassInfo(
    conf['Open-NEIS-API']['KEY'],
    conf['Open-NEIS-API']['SD_SCHUL_CODE'],
    conf['Open-NEIS-API']['ATPT_OFCDC_SC_CODE']
)
mod_eventinfo = EventInfo.EventInfo(
    conf['Open-NEIS-API']['KEY'],
    conf['Open-NEIS-API']['SD_SCHUL_CODE'],
    conf['Open-NEIS-API']['ATPT_OFCDC_SC_CODE']
)
mod_weather = Weather.Weather(
    conf['KMA-Weather-Api']['ZoneID']
)
mod_naver = Naver.Naver()

mutex = threading.Lock()
draw_mutex = threading.Lock()
log_file = open('log.log', 'wt')

class WeatherShow(Show.Show):
    show_name = 'Weather show'
    weather = mod_weather
    period = datetime.timedelta(hours=1, minutes=30)
    img = {}
    mutex = mutex
    
    def Load(self):
        def w(n):
            return self.W * n / 100
        def h(n):
            return self.H * n / 100
        self.fontH = self.H // 16
        self.font = pygame.font.Font(sys.path[0]+'/NanumSquare_acB.ttf', self.fontH)
    
        self.img['clear_day'] = pygame.image.load(sys.path[0]+"/weather/clear_day.jpg")
        self.img['clear_night'] = pygame.image.load(sys.path[0]+"/weather/clear_night.jpg")
        self.img['cloud'] = pygame.image.load(sys.path[0]+"/weather/cloud.jpg")
        self.img['cloud_day'] = pygame.image.load(sys.path[0]+"/weather/cloud_day.jpg")
        self.img['cloud_night'] = pygame.image.load(sys.path[0]+"/weather/cloud_night.jpg")
        self.img['rainy_cloud'] = pygame.image.load(sys.path[0]+"/weather/rainy_cloud.jpg")
        self.img['rainy_day'] = pygame.image.load(sys.path[0]+"/weather/rainy_day.jpg")
        self.img['rainy_night'] = pygame.image.load(sys.path[0]+"/weather/rainy_night.jpg")
        self.img['snow_cloud'] = pygame.image.load(sys.path[0]+"/weather/snow_cloud.jpg")
        self.img['snow_day'] = pygame.image.load(sys.path[0]+"/weather/snow_day.jpg")
        self.img['snow_night'] = pygame.image.load(sys.path[0]+"/weather/snow_night.jpg")
        self.img['sonagi_cloud'] = pygame.image.load(sys.path[0]+"/weather/sonagi_cloud.jpg")
        self.img['sonagi_day'] = pygame.image.load(sys.path[0]+"/weather/sonagi_day.jpg")
        self.img['sonagi_night'] = pygame.image.load(sys.path[0]+"/weather/sonagi_night.jpg")
        self.img['windy_cloud'] = pygame.image.load(sys.path[0]+"/weather/windy_cloud.jpg")
        self.img['windy_day'] = pygame.image.load(sys.path[0]+"/weather/windy_day.jpg")
        self.img['windy_night'] = pygame.image.load(sys.path[0]+"/weather/windy_night.jpg")

        for key in self.img.keys():
            self.img[key] = pygame.transform.scale(self.img[key], (int(w(70)), int(w(70))))
    
    def Render(self, dt):
        def w(n):
            return self.W * n / 100
        def h(n):
            return self.H * n / 100
        
        self.surf.fill((1, 1, 1))

        if not self.isEmpty:
            data = self.weather.data[0]

            
            day = True if 6 < int(data['hour']) < 18 else False
            sky = int(data['sky'])
            pty = int(data['pty'])
            wind_speed = float(data['ws'])
            pop = int(data['pop'])
            reh = int(data['reh'])

            mint = int(float(data['tmn']))
            mint = str(mint) if mint != -999 else '- '
            maxt = int(float(data['tmx']))
            maxt = str(maxt) if maxt != -999 else '- '
            nowt = data['temp']

            target = 'windy_night'
            
            if pty == 0:
                if wind_speed > 3:
                    if sky == 1:
                        target = 'windy_day'
                    elif sky == 3:
                        target = 'windy_night'
                    elif sky == 4:
                        target = 'windy_cloud'
                else:
                    if sky == 1:
                        target = 'clear_day'
                    elif sky == 3:
                        target = 'clear_night'
                    elif sky == 4:
                        target = 'cloud'
            elif pty == 1 or pty == 2:
                if sky == 1 or sky == 2:
                    target = 'rainy_day' if day else 'rainy_night'
                elif sky == 4:
                    target = 'rainy_cloud'
            elif pty == 3:
                if sky == 1 or sky == 3:
                    target = 'snow_day' if day else 'snow_night'
                elif sky == 4:
                    target = 'snow_cloud'
            elif ptr == 4:
                if sky == 1 or sky == 3:
                    target = 'sonagi_day' if day else 'sonagi_night'
                elif sky == 4:
                    target = 'sonagi_cloud'
            

            y = (self.H - (w(70) + (self.fontH * 1.6) * 3)) / 2
            self.surf.blit(self.img['windy_cloud'], ((w(100) - w(70)) / 2, y))
            y += w(70)
            
            text = self.font.render('%4s℃(%4s/%4s)'%(nowt, mint, maxt), True, (255, 255, 255))
            self.surf.blit(text, (w(50) - text.get_width() / 2, y - self.fontH / 2))
            y += self.fontH * 1.2
            text = self.font.render('%4s %3d%%' % ('　습도　',reh), True, (255, 255, 255))
            self.surf.blit(text, (w(50) - text.get_width() / 2, y - self.fontH / 2))
            y += self.fontH * 1.2
            text = self.font.render('%4s %3d%%' % ('강수확률',pop), True, (255, 255, 255))
            self.surf.blit(text, (w(50) - text.get_width() / 2, y - self.fontH / 2))
        
        return self.surf
    
    
    def Refresh(self):
        try:
            self.weather.get()
            self.isEmpty = False
        except Exception as e:
            self.mutex.acquire()
            print(e)
            print('%s %s'%(str(datetime.datetime.now()), str(e)))
            self.mutex.release()
            self.err_fresh = str(e)
            pass

class MealShow(Show.Show):
    show_name = 'Meal show'
    meal = mod_mealinfo
    period = datetime.timedelta(hours=3, minutes=0)
    img = {}
    mutex = mutex

    def Load(self):
        def w(n):
            return self.W * n / 100
        def h(n):
            return self.H * n / 100

        self.fontH = self.H // 20
        self.font = pygame.font.Font(sys.path[0]+'/NanumSquare_acB.ttf', self.fontH)
        self.fontBigH = self.H // 15
        self.fontBig = pygame.font.Font(sys.path[0]+'/NanumSquare_acB.ttf', self.fontBigH)
    
    def Render(self, dt):
        def w(n):
            return self.W * n / 100
        def h(n):
            return self.H * n / 100
        
        self.surf.fill((1, 1, 1))

        if not self.isEmpty:
            y = (self.H - (self.fontBigH * 1.5 + (self.fontH * 1.2) * 3)) / 2

            text = self.fontBig.render('%2d월 %2d일 %s' % (self.date.month, self.date.day, self.dish), True, (255, 255, 255))
            self.surf.blit(text, (w(50) - text.get_width() / 2, y - self.fontBigH / 2))
            y += self.fontBigH * 1.5
            rows = self.data['DDISH_NM'].split('<br/>')
            for row in rows:
                for num in range(14):
                    row = row.replace('%d.' % (14 - num), '')
                text = self.font.render(row, True, (255, 255, 255))
                self.surf.blit(text, (w(50) - text.get_width() / 2, y - self.fontH / 2))
                y += self.fontH * 1.2
        return self.surf
    
    
    def Refresh(self):
        try:
            now = datetime.datetime.now()
            

            if now < (datetime.datetime(year=now.year,month=now.month,day=now.day,hour=7,minute=30) if now.weekday() < 5 else datetime.datetime(year=now.year,month=now.month,day=now.day,hour=8,minute=20)):
                self.meal.set_date(now.year, now.month)
                self.data = self.meal.get(now.day)[0]
                self.date = now
                self.dish = '아'
            elif now < datetime.datetime(year=now.year,month=now.month,day=now.day,hour=12,minute=40):
                self.meal.set_date(now.year, now.month)
                self.data = self.meal.get(now.day)[1]
                self.date = now
                self.dish = '점심'
            elif now < datetime.datetime(year=now.year,month=now.month,day=now.day,hour=18,minute=40):
                self.meal.set_date(now.year, now.month)
                self.data = self.meal.get(now.day)[2]
                self.date = now
                self.dish = '저녁'
            else:
                tommorow = datetime.datetime.now() + datetime.timedelta(days=1)
                self.meal.set_date(tommorow.year, tommorow.month)
                self.data = self.meal.get(tommorow.day)[0]
                self.date = tommorow
                self.dish = '아침'
            self.isEmpty = False
        except Exception as e:
            self.mutex.acquire()
            print(e)
            print('%s %s'%(str(datetime.datetime.now()), str(e)))
            self.mutex.release()
            self.err_fresh = str(e)
            pass

class EventShow(Show.Show):
    show_name = 'Event show'
    event = mod_eventinfo
    period = datetime.timedelta(hours=6, minutes=0)
    img = {}
    mutex = mutex

    def Load(self):
        def w(n):
            return self.W * n / 100
        def h(n):
            return self.H * n / 100

        self.fontTitleH = self.H // 20
        self.fontTitle = pygame.font.Font(sys.path[0]+'/NanumSquare_acB.ttf', self.fontTitleH)
        self.fontDayH = int(self.W * 0.6)
        self.fontDay = pygame.font.Font(sys.path[0]+'/NanumSquare_acB.ttf', self.fontDayH)
        self.fontListH = self.H // 30
        self.fontList = pygame.font.Font(sys.path[0]+'/NanumSquare_acB.ttf', self.fontListH)

        self.wd2text = ['월','화','수','목','금','토','일']
        self.dweek = ['다음주']
    def Render(self, dt):
        def w(n):
            return self.W * n / 100
        def h(n):
            return self.H * n / 100
        
        self.surf.fill((1, 1, 1))
        
        y = h(5)
            
        
        if not self.isEmpty:
            text = self.fontTitle.render('%4d년 %2d월 %s요일' % (self.now.year, self.now.month, self.wd2text[self.now.weekday()]), True, (255, 255, 255))
            self.surf.blit(text, (w(50) - text.get_width() / 2, y))
            y += self.fontTitleH
            
            text = self.fontDay.render('%2d' % (self.now.day), True, (255, 255, 255))
            self.surf.blit(text, (w(50) - text.get_width() / 2, y))
            y += self.fontDayH

            for row in self.data:
                holiday = False    
                if row['SBTR_DD_SC_NM'] == '공휴일':
                    holiday = True
                if row['SBTR_DD_SC_NM'] == '휴업일':
                    holiday = True

                year = int(row['AA_YMD'][0:4])
                month = int(row['AA_YMD'][4:6])
                day = int(row['AA_YMD'][6:8])

                date = datetime.datetime(year = year, month = month, day = day, hour = self.now.hour, minute = self.now.minute, second = self.now.second, microsecond = self.now.microsecond)
                dt = date - self.now
                if dt.days == 0:
                    text = self.fontList.render('오늘',  True, (255, 255, 255))
                else:
                    if dt.days < 7:
                        text = self.fontList.render('%d일후 (%s)' % (dt.days, self.wd2text[date.weekday()]),  True, (255, 255, 255))
                    else:
                        text = self.fontList.render('%s (%s)' % (self.dweek[dt.days // 7 - 1] if (dt.days // 7 - 1) < len(self.dweek) else '%d주 후 %2d/%2d' % (dt.days // 7, date.month, date.day), self.wd2text[date.weekday()]),  True, (255, 255, 255))
                        
                #text = self.fontList.render('%s' % (('오늘' if dt.days == 0 else (')) if dt.days < 7 else '%d주후 %s요일' % (dt.days // 7, self.wd2text[date.weekday()])))), True, (255, 255, 255))
                self.surf.blit(text, (w(5), y))
                text = self.fontList.render(row['EVENT_NM'].strip() + ' ' + row['TARGET'], True, (255, 255, 255) if not holiday else (255, 128, 128))
                self.surf.blit(text, (w(95) - text.get_width(), y))
                y += self.fontListH + 10
        return self.surf
    def Refresh(self):
        try:
            now = datetime.datetime.now()
            self.now = now
            mod_eventinfo.load()
            self.data = mod_eventinfo.get(now.year, now.month, now.day, 12)
            self.isEmpty = False
        except Exception as e:
            self.mutex.acquire()
            print(e)
            print('%s %s'%(str(datetime.datetime.now()), str(e)))
            self.mutex.release()
            self.err_fresh = str(e)
            pass


class TimeTableShow(Show.Show):
    show_name = 'TimeTable show'
    period = datetime.timedelta(hours=5, minutes=0)
    img = {}
    _class = mod_classinfo
    target_grade = 2
    target_class = 3
    mutex = mutex

    def Load(self):
        def w(n):
            return self.W * n / 100
        def h(n):
            return self.H * n / 100

        self.fontTitleH = self.H // 18
        self.fontTitle = pygame.font.Font(sys.path[0]+'/NanumSquare_acB.ttf', self.fontTitleH)
        
        self.fontListH = self.H // 35
        self.fontList = pygame.font.Font(sys.path[0]+'/NanumSquare_acB.ttf', self.fontListH)
        self.wd2text = ['월','화','수','목','금','토','일']
    def Render(self, dt):
        def w(n):
            return self.W * n / 100
        def h(n):
            return self.H * n / 100
        
        self.surf.fill((1, 1, 1))
        
        y = (self.H - (self.fontTitleH * 2 + self.fontListH * 1.6 * 9)) / 2
            
        
        if not self.isEmpty:
            text = self.fontTitle.render('%d학년 %d반 (%s)시간표 ' % (self.target_grade, self.target_class, self.wd2text[self.now.weekday()]),  True, (255, 255, 255))
            self.surf.blit(text, (w(50) - text.get_width() // 2, y))
            y += self.fontTitleH * 2

            table = {}
            for row in self._class.get(self.target_grade, self.target_class):
                table[int(row['PERIO'])] = row['ITRT_CNTNT']
            i = 1
            for _ in range(9):
                text = self.fontList.render('%d교시' % (i),  True, (255, 255, 255))
                self.surf.blit(text, (w(10), y))
                
                text = self.fontList.render(table[i] if i in table else '정보 없음' ,  True, (255, 255, 255))
                self.surf.blit(text, (w(90) - text.get_width(), y))
                y += self.fontListH * 1.6
                i += 1
        return self.surf
    def Refresh(self):
        try:
            now = datetime.datetime.now()
            self.now = now
            self._class.set_date(now.year, now.month, now.day)
            self.isEmpty = False
        except Exception as e:
            self.mutex.acquire()
            print(e)
            print('%s %s'%(str(datetime.datetime.now()), str(e)))
            self.mutex.release()
            self.err_fresh = str(e)
            pass

class ClockShow(Show.Show):
    show_name = 'Clock show'
    period = datetime.timedelta(hours=0, minutes=0, seconds=31)
    img = {}
    times = []
    data = ''
    mutex = mutex

    def add_time(self,hour, minute, sub,tag=''):
        obj = {'h' : hour, 'm' : minute, 'sub' : sub, 'tag' : tag}
        self.times.append(obj)

    def Load(self):
        def w(n):
            return self.W * n / 100
        def h(n):
            return self.H * n / 100

        self.fontTitleH = self.H // 10
        self.fontTitle = pygame.font.Font(sys.path[0]+'/NanumSquare_acB.ttf', self.fontTitleH)
        self.fontLefttimeH = self.H // 18
        self.fontLefttime = pygame.font.Font(sys.path[0]+'/NanumSquare_acB.ttf', self.fontLefttimeH)
        self.fontNextH = self.H // 23
        self.fontNext = pygame.font.Font(sys.path[0]+'/NanumSquare_acB.ttf', self.fontNextH)
        self.fontClockH = self.H // 6
        self.fontClock = pygame.font.Font(sys.path[0]+'/NanumSquare_acB.ttf', self.fontClockH)

        self.add_time(6,20,'기상',tag='{평일}{아침}')
        self.add_time(6,30,"아침점호",tag='{평일}{아침}')
        self.add_time(7,20,'아침 식사',tag='{평일}{아침}')
        self.add_time(7,50,'등교',tag='{평일}{자율}')
        self.add_time(8,30,'조례',tag='{평일}')
        
        self.add_time(8,40,'1교시',tag='{평일}')
        self.add_time(9,30,'쉬는시간',tag='{평일}{자율}')
        self.add_time(9,40,'2교시',tag='{평일}')
        self.add_time(10,30,'쉬는시간',tag='{평일}{자율}')
        self.add_time(10,40,'3교시',tag='{평일}{점심}')
        self.add_time(11,30,'쉬는시간',tag='{평일}{점심}{자율}')
        self.add_time(11,40,'4교시',tag='{평일}{점심}')
        self.add_time(12,30,'점심시간',tag='{평일}{점심}{자율}')
        
        
        self.add_time(13,20,'5교시',tag='{평일}')
        self.add_time(14,10,'쉬는시간',tag='{평일}{자율}')
        self.add_time(14,20,'6교시',tag='{평일}')
        self.add_time(15,10,'쉬는시간',tag='{평일}{자율}')
        self.add_time(15,20,'7교시',tag='{평일}')
        
        self.add_time(16,10,'종례 및 청소',tag='{평일}{저녁}')
        
        self.add_time(16,30,'8교시',tag='{평일}{저녁}')
        self.add_time(17,20,'쉬는시간',tag='{평일}{저녁}{자율}')
        self.add_time(17,30,'9교시',tag='{평일}{저녁}')
        
        self.add_time(18,20,'저녁시간',tag='{평일}{저녁}{자율}')
        self.add_time(19,10,'자율1교시',tag='{평일}')
        self.add_time(20,00,'쉬는시간',tag='{평일}{자율}')
        self.add_time(20,10,'자율2교시',tag='{평일}')

        self.add_time(21,00,'기숙사 이동',tag='{평일}{자율}')
        self.add_time(21,15,'개인시간',tag='{평일}{자율}')
        self.add_time(21,40,'저녁점호',tag='{평일}')
        self.add_time(21,50,'개인시간',tag='{평일}')
        self.add_time(22,10,'심야자습',tag='{평일}')
        self.add_time(22,45,'숙면준비',tag='{평일}')
        self.add_time(23,00,'',tag='{평일}')

        self.add_time( 8,10,'아침점호',tag='{휴일}{아침}')
        self.add_time( 8,30,'오전일과',tag='{휴일}{자율}{점심}')
        self.add_time(12,30,'점심시간',tag='{휴일}{자율}{점심}')
        self.add_time(13,20,'오후일과',tag='{휴일}{자율}{저녁}')
        self.add_time(17,00,'복귀신고',tag='{휴일}{자율}{저녁}')
        self.add_time(18,00,'저녁시간',tag='{휴일}{자율}{저녁}')
        self.add_time(19,10,'야간일과',tag='{휴일}{자율}')
        self.add_time(21,15,'개인시간',tag='{휴일}{자율}')
        self.add_time(21,40,'저녁점호',tag='{휴일}')
        self.add_time(21,50,'개인시간',tag='{휴일}')
        self.add_time(22,10,'심야자습',tag='{휴일}')
        self.add_time(22,45,'숙면준비',tag='{휴일}')
        self.add_time(23,00,'',tag='{휴일}')
        
    def Render(self, dt):
        def w(n):
            return self.W * n / 100
        def h(n):
            return self.H * n / 100
        
        self.surf.fill((1, 1, 1))
        
        y = (self.H - (self.fontClockH * 1.2 + self.fontTitleH + self.fontLefttimeH + self.fontNextH + h(7))) / 2
        
        if not self.isEmpty:
            text = self.fontClock.render('%02d:%02d' % (self.now.hour, self.now.minute),  True, (255, 255, 255))
            self.surf.blit(text, (w(50) - text.get_width() // 2, y))
            y += self.fontClockH * 1.2
            
            text = self.fontTitle.render(str(self.desc),  True, (255, 255, 255))
            self.surf.blit(text, (w(50) - text.get_width() // 2, y))
            y += self.fontTitleH

            sec = self.left_time.seconds
            mit = sec // 60
            sec = sec % 60
            hour = mit // 60
            mit = mit % 60
            hour = hour % 24
            s = ''
            if hour > 0:
                s += str(hour) + 'hrs '
            s += str(mit) + 'min'
            s = '(%s)' % s
            
            text = self.fontLefttime.render(s,  True, (255, 255, 255))
            self.surf.blit(text, (w(50) - text.get_width() // 2, y))
            y += self.fontLefttimeH + h(7)
            text = self.fontNext.render('다음시간>> ' + self.next_desc,  True, (155, 155, 155))
            self.surf.blit(text, (w(50) - text.get_width() // 2, y))
            y += self.fontNextH
        return self.surf
    def Refresh(self):
        try:
            now = datetime.datetime.now()
            holiday = False if now.weekday() < 5 else True


            now_time = datetime.datetime(year=2002,month=1,day=1, hour=now.hour, minute=now.minute)
            start_time_name = ''
            end_time_name = ''
            start_time = datetime.datetime(year=2002,month=1,day=1, hour = 0, minute = 0)
            end_time = datetime.datetime(year=2002,month=1,day=1, hour = 23, minute = 59)

            for time in self.times:
                if (time['tag'].find('{휴일}') != -1 and holiday) or (time['tag'].find('{휴일}') == -1 and (not holiday)):
                    this_time = datetime.datetime(year=2002,month=1,day=1, hour = time['h'], minute = time['m'])
                    if this_time < now_time:
                        if this_time > start_time:
                            start_time = this_time
                            start_time_name = time['sub']
            for time in self.times:
                if (time['tag'].find('{휴일}') != -1 and holiday) or (time['tag'].find('{휴일}') == -1 and (not holiday)):
                    this_time = datetime.datetime(year=2002,month=1,day=1, hour = time['h'], minute = time['m'])
                    if this_time > start_time:
                        if this_time < end_time:
                            end_time = this_time
                            end_time_name = time['sub']

            self.now = now
            self.desc = start_time_name
            self.next_desc = end_time_name
            self.left_time = end_time - now_time
            self.isEmpty = False
        except Exception as e:
            self.mutex.acquire()
            print(e)
            print('%s %s'%(str(datetime.datetime.now()), str(e)))
            self.mutex.release()
            self.err_fresh = str(e)
            pass

class NaverShow(Show.Show):
    show_name = 'Naver show'
    period = datetime.timedelta(hours=1, minutes=30)
    img = {}
    naver = mod_naver
    mutex = mutex
    
    def Load(self):
        def w(n):
            return self.W * n / 100
        def h(n):
            return self.H * n / 100

        self.fontTitleH = self.H // 16
        self.fontTitle = pygame.font.Font(sys.path[0]+'/NanumSquare_acB.ttf', self.fontTitleH)
        
        self.fontListH = self.H // 24
        self.fontList = pygame.font.Font(sys.path[0]+'/NanumSquare_acB.ttf', self.fontListH)
        self.highRankX = 0
        self.lowRankX = 0.5
        self.animateProgress = 0
        self.animateType = 'left'
        self.stop = 0
        self.stop_time = 10
    def Render(self, dt):
        def w(n):
            return self.W * n / 100
        def h(n):
            return self.H * n / 100
        
        self.surf.fill((1, 1, 1))
        if not self.isEmpty:
            if self.stop < 0:
                if self.animateType == 'left':
                    self.animateProgress -= dt * ((self.animateProgress ** 2) * 5 + 0.6)
                    if self.animateProgress < 0:
                        self.animateProgress = 0
                        self.animateType = 'right'
                        self.stop = self.stop_time
                elif self.animateType == 'right':
                    self.animateProgress += dt * (((1 - self.animateProgress) ** 2) * 5 + 0.6)
                    if self.animateProgress > 1:
                        self.animateProgress = 1
                        self.animateType = 'left'
                        self.stop = self.stop_time
            else:
                self.stop -= dt
                
            self.highRankX = (self.animateProgress ** 2) - 1
            self.lowRankX = (self.animateProgress ** 2)
        
        
            y = (self.H - (self.fontListH * 1.6 * 10 + self.fontTitleH * 3)) / 2
        
            text = self.fontTitle.render('실시간 급상승 검색어',  True, (255, 255, 255))
            self.surf.blit(text, (w(50) - text.get_width() // 2, y))
            y += self.fontTitleH * 3

            y_copied = y
            for _ in range(10):
                text = self.fontList.render(self.naver.data[_][:10],  True, (255, 255, 255))
                self.surf.blit(text, (w(95) - text.get_width()+ w(100) * self.highRankX, y))
                text = self.fontList.render('%d위' % (_ + 1),  True, (255, 255, 255))
                self.surf.blit(text, (w(5)+ w(100) * self.highRankX, y))
                y += self.fontListH * 1.6

            y = y_copied
            for _ in range(10):
                text = self.fontList.render(self.naver.data[10 + _][:10],  True, (255, 255, 255))
                self.surf.blit(text, (w(95) - text.get_width() + w(100) * self.lowRankX , y))
                text = self.fontList.render('%d위' % (_ + 11),  True, (255, 255, 255))
                self.surf.blit(text, (w(5) + w(100) * self.lowRankX, y))
                y += self.fontListH * 1.6
            
        return self.surf
    def Refresh(self):
        try:
            now = datetime.datetime.now()
            self.now = now
            self.naver.get()
            self.isEmpty = False
        except Exception as e:
            self.mutex.acquire()
            print(e)
            print('%s %s'%(str(datetime.datetime.now()), str(e)))
            self.mutex.release()
            self.err_fresh = str(e)
            pass
        
class WatchShow(Show.Show):
    show_name = 'Watch show'
    period = datetime.timedelta(hours=0, minutes=0, seconds=0,microseconds=500000)
    img = {}
    _class = mod_classinfo
    mutex = mutex
    target_hour = 0

    def Load(self):
        def w(n):
            return self.W * n / 100
        def h(n):
            return self.H * n / 100

        self.fontTitleH = self.H // 18
        self.fontTitle = pygame.font.Font(sys.path[0]+'/NanumSquare_acB.ttf', self.fontTitleH)
        self.fontDescH = self.H // 30
        self.fontDesc = pygame.font.Font(sys.path[0]+'/NanumSquare_acB.ttf', self.fontDescH)
        
    def Render(self, dt):
        def w(n):
            return self.W * n / 100
        def h(n):
            return self.H * n / 100
        
        self.surf.fill((1, 1, 1))
                   
        
        if not self.isEmpty:
            y = (self.H - (w(90) + self.fontTitleH * 1.8 + self.fontDescH)) // 2
            pygame.draw.ellipse(self.surf, (180, 180, 180), (w(5),y,w(90), w(90)), 5)

            for _ in range(12):
                rad = _ / 6 * math.pi - math.pi / 2
                pygame.draw.line(self.surf, (160, 160, 160),
                (w(50) + math.cos(rad) * w(40), y + w(45) + math.sin(rad) * w(40)),
                (w(50) + math.cos(rad) * w(43), y + w(45) + math.sin(rad) * w(43)), 3)
            
            rad = self.now.second / 30 * math.pi - math.pi / 2
            pygame.draw.line(self.surf, (255, 0, 0), (w(50), y + w(45)),
            (w(50) + math.cos(rad) * w(40), y + w(40) + math.sin(rad) * w(40)), 3)
            
            rad = self.now.minute / 30 * math.pi - math.pi / 2
            pygame.draw.line(self.surf, (255, 255, 255), (w(50), y + w(45)),
            (w(50) + math.cos(rad) * w(36), y + w(45) + math.sin(rad) * w(36)), 10)
            
            rad = self.now.hour / 6 * math.pi - math.pi / 2
            pygame.draw.line(self.surf, (255, 255, 255), (w(50), y + w(45)),
            (w(50) + math.cos(rad) * w(32), y + w(45) + math.sin(rad) * w(32)), 16)
            
            y += w(90)

            text = self.fontTitle.render('%02d:%02d:%02d' % (now.hour, now.minute, now.second),  True, (255, 255, 255))
            self.surf.blit(text, (w(50) - text.get_width() // 2, y))
            y += self.fontDescH * 1.8
            
            text = self.fontDesc.render('스마트 미러에서 %2d시를 알려드립니다.' % (self.target_hour),  True, (255, 255, 255))
            self.surf.blit(text, (w(50) - text.get_width() // 2, y))
            y += self.fontDescH
            
        return self.surf
    def Refresh(self):
        try:
            now = datetime.datetime.now()
            self.now = now
            self.isEmpty = False
        except Exception as e:
            self.mutex.acquire()
            print(e)
            print('%s %s'%(str(datetime.datetime.now()), str(e)))
            self.mutex.release()
            self.err_fresh = str(e)
            pass
        
pygame.init()
pygame.mixer.init()
WND_W = 768 // 2
WND_H = 1366 // 2
surf = pygame.display.set_mode((WND_W, WND_H), pygame.FULLSCREEN if False else 0)
       
SHOWS = {}
SHOWS[0] = WeatherShow(WND_W, WND_H)
SHOWS[1] = MealShow(WND_W, WND_H)
SHOWS[2] = EventShow(WND_W, WND_H)
SHOWS[3] = TimeTableShow(WND_W, WND_H)
SHOWS[4] = ClockShow(WND_W, WND_H)
SHOWS[5] = NaverShow(WND_W, WND_H)
SHOWS[6] = WatchShow(WND_W, WND_H)
for _ in range(len(SHOWS)):
    while SHOWS[_].isEmpty: time.sleep(0.1)
    SHOWS[_].isPause = True
SHOWS[0].isPause = False
SHOWS[1].isPause = False

class ManagerShow(Show.Show):
    show_name = 'Manager show'
    period = datetime.timedelta(hours=0, minutes=0, seconds=3)
    mutex = mutex
    draw_mutex = draw_mutex
    img = {}
    num_of_show = len(SHOWS)

    def Load(self):
        def w(n):
            return self.W * n / 100
        def h(n):
            return self.H * n / 100

        self.ShowA = 0
        self.ShowB = 1
        self.ShowAAlpha = 1
        self.ShowBAlpha = 0
        self.AnimateProgress = 0

    def Render(self, dt):
        now = datetime.datetime.now()
        #print(5)

        if now.second >= 57 and (now.minute == 59) :
            if self.ShowA != 6 and self.ShowB != 6:
                #print(7)
                draw_mutex.acquire()
                SHOWS[6].target_hour = now.hour + 1
                SHOWS[self.ShowB].isPause = True
                self.ShowB = self.ShowA
                self.ShowBAlpha = 1
                self.ShowA = 6
                SHOWS[self.ShowA].isPause = False
                self.ShowAAlpha = 0
                self.AnimateProgress = 0
                pygame.mixer.music.load(sys.path[0]+'/beep.mp3')
                pygame.mixer.music.set_volume(0.2)
                pygame.mixer.music.play()
                draw_mutex.release()
                #print(77)
        elif self.ShowA == 6 and now.second >= 1 and now.second < 57:
            #print(8)
            draw_mutex.acquire()
            SHOWS[self.ShowB].isPause = True
            self.ShowB = self.ShowA
            self.ShowBAlpha = 1
            self.ShowA = 0
            SHOWS[self.ShowA].isPause = False
            self.ShowAAlpha = 0
            self.AnimateProgress = 0
            #self.last_refresh = now
            draw_mutex.release()
            #print(88)
        elif now - self.last_refresh > self.period:
            #print(9)
            draw_mutex.acquire()
            #print('find new slide')
            SHOWS[self.ShowB].isPause = True
            self.ShowB = self.ShowA
            self.ShowBAlpha = 1
            #print('find start')
            
            target = (self.ShowB + 1) % self.num_of_show
            while target == 6: target = (target + 1) % self.num_of_show
            mutex.acquire()
            print(target)
            mutex.release()
            self.ShowA = target
            SHOWS[self.ShowA].isPause = True
            self.ShowAAlpha = 0
            self.AnimateProgress = 0
            self.last_refresh = now
            draw_mutex.release()
        
        #print('55')
    def Refresh(self):
        try:
            #self.isEmpty = False
            pass
        except Exception as e:
            print(e)
            print('%s %s'%(str(datetime.datetime.now()), str(e)))
            self.err_fresh = str(e)
            pass
        
SHOW_MNG = ManagerShow(WND_W, WND_H)

def w(n):
    return WND_W * n / 100
def h(n):
    return WND_H * n / 100

loop = True
FORE_COLOR = (255, 255, 255)
i = 0
t = datetime.datetime.now()
tick = datetime.datetime.now()
while loop:
    now = datetime.datetime.now()
    dt = (now - tick).microseconds / 1000000
    tick = now

    if (datetime.datetime.now() - t).seconds >= 1:
        t =  datetime.datetime.now()
        pygame.display.set_caption(str(i))
        i = 0
    i += 1
    for e in pygame.event.get():
        if e.type == pygame.locals.QUIT:
            loop = False
        elif e.type == pygame.locals.KEYDOWN:
            if e.key == pygame.locals.K_a:
                loop = False

    surf.fill((0, 0, 0))
    #pygame.draw.rect(surf, FORE_COLOR, ((w(100) - w(70)) / 2, (h(100) - w(70)) / 2, w(70), w(70)))
    
    SHOW_MNG.Render(dt)
    #print(6)
    if now.hour < 23 and now.hour > 6:
        draw_mutex.acquire()
        if SHOW_MNG.ShowBAlpha > 0:
            s = SHOWS[SHOW_MNG.ShowB].Render(dt)
            s.set_alpha(int(255 * SHOW_MNG.ShowBAlpha))
            surf.blit(s, (0, 0))
            
            SHOW_MNG.ShowBAlpha = (1 - SHOW_MNG.AnimateProgress) ** 6
            SHOW_MNG.ShowAAlpha = SHOW_MNG.AnimateProgress ** 6
            SHOW_MNG.AnimateProgress += dt
            
            if SHOW_MNG.AnimateProgress > 1:
                SHOW_MNG.ShowAAlpha = 1
                SHOW_MNG.ShowBAlpha = 0
            
        if SHOW_MNG.ShowAAlpha > 0:
            s = SHOWS[SHOW_MNG.ShowA].Render(dt)
            s.set_alpha(int(255 * SHOW_MNG.ShowAAlpha))
            surf.blit(s, (0, 0))

        draw_mutex.release()
    #print(66)
    pygame.display.flip()

for _ in SHOWS:
    SHOWS[_].flagQuit = True

pygame.mixer.quit()
pygame.quit()
log_file.close()

