"""
#Created 27/02/2021
@author: andrewdarby

represents collection of files on filesystem
"""
import pathlib
import os
import re
import math
import datetime
from os import system, name

class Files():
    def __init__(self):
        # initalise files obj
        self.filesPerSecton = {} # Dict of fileinfo

    def findfiles(self,directory,baseurl,allfiles,secondaryfiles,termdates):
    # Walk the files folder.
        for folder, directories, files in os.walk(directory):         

            print(f'folder {folder}')
            x = re.search(r"t(\d{1,2}).*wk(\d{1,2}).*$", folder)
            if x is None:
                continue  
            termno = int(x.group(1))
            weekno = int(x.group(2))
            if (termno > 1):
                termstart = datetime.datetime.strptime(termdates[termno-1], '%Y-%m-%d')  
                yearstart = datetime.datetime.strptime(termdates[0], '%Y-%m-%d')
                tdelta = (termstart - yearstart)
                weekdiff = math.ceil(tdelta.days/7)
            else:
                weekdiff = 0
            sectionid = weekno + weekdiff
                
            maxfiles = len(files)
            for count in range(0,maxfiles):
                filename = files[count]
                
                # Join the two strings in order to form the full filepath.
                filepath = os.path.join(folder, filename)
                ext = pathlib.Path(filepath).suffix
                
                foldername = os.path.basename(folder)
 
                append = True
                lectures_append = False
                # if entry for this section in filesperweek, retrieve that dict
                if sectionid in self.filesPerSecton: 
                    fileinfo = self.filesPerSecton[sectionid]
                # else create new fileinfo to append to collection
                else:
                    fileinfo = {"termno": termno, "weekno": weekno, "sectionid": sectionid,"folders": [], "lectureslides": [], "extrafiles": [] }

                foldersthisweek = fileinfo['folders']
                if (foldername not in foldersthisweek):
                    fileinfo['folders'].append(foldername) # update folders for this week
                    lectures_append = True
                    lectureslides = {"folder": foldername, "mdtitle":"", "htmltitle": "", "slidesurl": "", "pdfslideurl": ""}
                else:
                    folder_no = len(fileinfo['folders'])
                    lectureslides = fileinfo['lectureslides'][folder_no-1]        
                
                if (ext in allfiles): # only update if one of selected files.
                    if (ext == ".md"):
                        # set title from md file markdown file
                        lectureslides['mdtitle'] = f"Week {weekno}: {self.mdfiletitle(filepath)}"
                    if (ext == ".html"):
                        # set title from html file (in case there was no md file)
                        lectureslides['htmltitle'] = self.htmlfiletitle(filepath)
                        lectureslides['slidesurl'] = os.path.join(baseurl, filepath).replace('\\','/').replace('/index.html','/')
                    
                    x = re.search(r"^wk\d{1,2}.*", filename)
                    if (ext == ".pdf" and x is not None):  # if filename is "wk{weekno}*.pdf" 
                            lectureslides["pdfslidesurl"] = os.path.join(baseurl, filepath).replace('\\','/')
                    elif (ext in secondaryfiles):
                        # include extra files if 'primary' wk{weekno} naming convention
                        extrafiles = fileinfo['extrafiles']
                        title = filename[0:len(filename)-4]
                        fileurl = os.path.join(baseurl, filepath).replace('\\','/')
                        extrafileinfo = {"title": title, "url": fileurl}
                        extrafiles.append(extrafileinfo)
                        fileinfo['extrafiles'] = extrafiles 
                    # save details
                    if (lectures_append):
                        fileinfo['lectureslides'].append(lectureslides)
                    else:
                        fileinfo['lectureslides'][folder_no-1] = lectureslides   
                    self.filesPerSecton[sectionid] = fileinfo                      
                    

    def FindNewContentUpload(self,sec):
        updatesections = []
        for lecture in self.lecturedetails:
            lecture_week_number = lecture['weekno']
            section = sec.getsections[lecture_week_number]
            if ((len(section['summary'])) == 0 and self.isNoAnchorTag(section['summary'])):
                summaryHTML = "new HTML" #-> function to build the HTML summary
                newsection = {"section": lecture_week_number, "summary": summaryHTML}
                updatesections.append(newsection)
                
    def isNoAnchorTag(self,text): # To complete
        return False
    
    def mdfiletitle(self,filepath):
        with open(filepath, 'r') as infile:
            for line in infile:
                x = re.search(r"#{2}\s(.*)$", line) ## match markdown title
                if (x is not None):
                    title = x.group(1)
                    if (title != ""):
                        return title 
        return ""
    
    def htmlfiletitle(self,filepath):
        with open(filepath, 'r',encoding="utf-8") as infile:
            for line in infile:
                x = re.search(r"<title>([^<]*)</title>$", line) ## match html title
                if (x is not None):
                    title = x.group(1)
                    if (title != ""):
                        return title 
        return ""
    
    def print(self):
        # iterate filesPerSecton dict.
        sections = self.filesPerSecton.values()
        for f in sections:
            print(f"Term: {f['termno']}, section {f['sectionid']}")
            #mdtitle
            lectureslides = f["lectureslides"]
            for s in lectureslides:
                print("-: md: {mdtitle}, html: {htmltitle}".format(mdtitle=s['mdtitle'], htmltitle = s['htmltitle']))
                print("-: url: {slidesurl}".format(slidesurl=s['slidesurl']))
                if (s['pdfslidesurl'] is not None):
                    print("-: pdf: {pdfslidesurl}".format(pdfslidesurl= s['pdfslidesurl']))
            for s in f['extrafiles']:
                print(f" ->> Extra {s['title']}, {s['url']}")