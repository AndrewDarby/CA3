"""
#Created 27/02/2021
@author: andrewdarby

represents collection of videos from google drive
"""
import datetime
import requests
import bs4

class Videos():
    def __init__(self):
        # initalise files obj
        self.videolinks = []  # List of files
        
    def findvideos(self,videourl,termdates):
        # get HTML
        res = requests.get(videourl)
        soup = bs4.BeautifulSoup(res.text,"lxml") # credit to Michael
        videos = soup.find_all('div',class_ = 'Q5txwe')
        for video in videos:
            video_id = video.parent.parent.parent.parent.attrs['data-id']
            text = video.text.split(" - ")
            video_title = text[1]
            date_obj = datetime.datetime.strptime(text[0], '%Y-%m-%d [%H:%M:%S]').date()
            videoinfo = { 'title': video_title, 'linkhash': video_id, 'date': date_obj}
            self.videolinks.append(videoinfo)

    def print(self):
        nop

#soup = bs4.BeautifulSoup(res.text,"lxml")
        # content using BS4
        # loop all entries, to create dictionary (date, title, filename, weekno)
        # decode date of the video. 