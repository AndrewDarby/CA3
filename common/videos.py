"""
#Created 27/02/2021
@author: andrewdarby

represents collection of videos from google drive
"""
import datetime
import requests
import bs4
import re
import math

VIDEOSPERSECTION =  {'videolinks': []}

class Videos():
    def __init__(self):
        # initalise files obj
        self.videolinks = []  # List of videos found
        self.videospersection = {}  # grouped by weekno
        
    def findvideos(self,videourl,termdates):
        # get HTML
        #res = requests.get(videourl)
        #soup = bs4.BeautifulSoup(res.text,"lxml")
        f = open("googlevideotxt.html", "r")
        #f.write(res.text)
        file=f.read().replace('\n', '')
        soup = bs4.BeautifulSoup(file,"lxml") 
        f.close()
        videos = soup.find_all('div',class_ = 'Q5txwe')
        for video in videos:
            video_id = video.parent.parent.parent.parent.attrs['data-id']  # credit to Michael
            title = video.text
            text = title.split("]")
            x = re.search(r"(\d{4}-\d{2}-\d{2})\s\[(\d{2}:\d{2})-(\d{2}:\d{2})", text[0])
            if x is None:
                continue  
            v_date = x.group(1)
            v_start = v_date + " ["+ x.group(2) + "]"
            v_end = v_date + " ["+ x.group(3) + "]"
            date_start = datetime.datetime.strptime(v_start, '%Y-%m-%d [%H:%M]')
            date_end = datetime.datetime.strptime(v_end, '%Y-%m-%d [%H:%M]')
            duration = self.getDuration(date_start,date_end) # include duration of video in title
            title = f'{date_start.date()} [{duration}] {text[1]}'
            terminfo = self.selectTermAndWeek(date_start,termdates)
            videoinfo = { 'title': title, 'linkhash': video_id, 'date': date_start.date(),'term': terminfo['term'], 'weekno': terminfo['weekno'], 'sectionid': terminfo['sectionid'] }
            self.videolinks.append(videoinfo)

    def sortvideosintosections(self):
        for v in self.videolinks:
            sectionId = int(v['sectionid'])
            if (sectionId in self.videospersection):
                videolist = self.videospersection[sectionId]['videolinks'] 
            else:
                videolist = []
                self.videospersection[sectionId] = VIDEOSPERSECTION.copy()
            videolist.append(v)
            self.videospersection[sectionId]['videolinks'] = videolist
                
              
    def printsections(self):
        for key in self.videospersection:
            print(f'## section: {key}')
            videos = self.videospersection[key]['videolinks']
            for v in videos:
                self.printinfo(v) 
            
    def printlinks(self):
            for v in self.videolinks:
                self.printinfo(v)    
        
    def printinfo(self,v):
        print("tite: {title}, hash:{linkhash}, date {videodate} term:{term}, weekno {weekno}, sectionid: {sectionid}"
                  .format(title=v['title'],linkhash=v['linkhash'],videodate=v['date'],term=v['term'],weekno=v['weekno'], sectionid=v['sectionid']))

    # determine which term video belongs to + weekno
    def selectTermAndWeek(self,file_start,termdates):
        term = 0
        weekno=0
        for x in range(len(termdates)-1,-1,-1):
            termdate = termdates[x]
            termstart = datetime.datetime.strptime(termdate, '%Y-%m-%d')
            tdelta = (file_start - termstart)
            if (tdelta.days > 0):
                term = x+1
                weekno = math.ceil(tdelta.days/7)
                break
        yearstart = datetime.datetime.strptime(termdates[0], '%Y-%m-%d')
        startyear_delta = (file_start - yearstart)
        sectionid = math.ceil(startyear_delta.days/7)
        return {'term':term, 'weekno':weekno, 'sectionid': sectionid}
        
    def getDuration(self,startDate, endDate):
        tdelta = (endDate - startDate)
        totalseconds = int(tdelta.seconds)
        hours, remainder = divmod(totalseconds,3600)
        minutes, seconds = divmod(remainder, 60)
        return f'{hours}h {minutes}m'
        