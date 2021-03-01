"""
#Created 27/02/2021
@author: andrewdarby

represents collection of files on filesystem
"""
import pathlib
import os
import re
from os import system, name

class Files():
    def __init__(self):
        # initalise files obj
        self.filesperweek = []  # List of files
        

    def findfiles(self,directory,baseurl,allfiles,secondaryfiles):
    # Walk the files folder.
        for folder, directories, files in os.walk(directory):
            
            x = re.search(r"(\d{1,2}).*$", folder)
            if x is None:
                continue  
            weekno = int(x.group(1))
                
            maxfiles = len(files)
            for count in range(0,maxfiles):
                filename = files[count]
                
                # Join the two strings in order to form the full filepath.
                filepath = os.path.join(folder, filename)
                ext = pathlib.Path(filepath).suffix
                
                foldername = os.path.basename(folder)
 
                append = True
                lectures_append = False
                # if second file this week, add to existing fileinfo
                if (len(self.filesperweek) >= weekno):
                    fileinfo = self.filesperweek[weekno-1]
                    
                    append = False
                # else create new fileinfo to append to collection
                else:
                    fileinfo = {"weekno": weekno, "folders": [], "lectureslides": [], "extrafiles": [] }

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
                        ##TODO++ fileinfo["htmltitle"] = "Week {weekno}: {htmlfiletitle(filepath)}"
                        lectureslides['htmltitle'] = self.htmlfiletitle(filepath)
                        lectureslides['slidesurl'] = os.path.join(baseurl, filepath).replace('\\','/').replace('/index.html','/')
                    
                    x = re.search(r"^wk\d{1,2}", filename)
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
                    if (append):
                        self.filesperweek.append(fileinfo)  # Add it to the collection
                    else:
                        self.filesperweek[weekno-1] = fileinfo  # Add it to the collection
                    

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
        # Walk the files folder.
            for f in self.filesperweek:
                print(f" {f['weekno']}")
                #mdtitle
                lectureslides = f["lectureslides"]
                for s in lectureslides:
                    print("-: md: {mdtitle}, html: {htmltitle}".format(mdtitle=s['mdtitle'], htmltitle = s['htmltitle']))
                    print("-: url: {slidesurl}".format(slidesurl=s['slidesurl']))
                    if (s['pdfslidesurl'] is not None):
                        print("-: pdf: {pdfslidesurl}".format(pdfslidesurl= s['pdfslidesurl']))
                for s in f['extrafiles']:
                    print(f" ->> Extra {s['title']}, {s['url']}")