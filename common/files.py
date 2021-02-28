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
            
            print("Currently looking at folder: "+ folder)
            print('\n')

            for filename in files:
                # Join the two strings in order to form the full filepath.
                filepath = os.path.join(folder, filename)
                ext = pathlib.Path(filepath).suffix
                x = re.search(r"\d{1,2}$", folder)
                if x is None:
                    continue
                    
                weekno = int(x.group(0))
                append = True
                # if second file this week, add to existing fileinfo
                if (len(self.filesperweek) >= weekno):
                    fileinfo = self.filesperweek[weekno-1]
                    append = False
                # else create new fileinfo to append to collection
                else:
                    fileinfo = {"folder":folder, "weekno": weekno, "extrafiles": [] }
                    
                if (ext in allfiles): # only update if one of selected files.
                    print(f"(1)found {filename}")
                    if (ext == ".md"):
                        # set title from md file markdown file
                        fileinfo["mdtitle"] = f"Week {weekno}: {self.mdfiletitle(filepath)}"
                    if (ext == ".html"):
                        # set title from html file (in case there was no md file)
                        ##TODO++ fileinfo["htmltitle"] = "Week {weekno}: {htmlfiletitle(filepath)}"
                        fileinfo["htmltitle"] = self.htmlfiletitle(filepath)
                        fileinfo["slidesurl"] = os.path.join(baseurl, filepath).replace('\\','/').replace('\\index.html','')
                    if (ext == ".pdf"):
                        # if filename is "wk{weekno}.pdf" add as main slidespdfurl
                        isWeekfile = (filename == f"wk{weekno}.pdf")
                        if (isWeekfile):
                            fileinfo["pdfslidesurl"] = os.path.join(baseurl, filepath).replace('\\','/')
                    if (ext in secondaryfiles):
                        # include extra files if 'primary' wk{weekno} naming convention
                        if (filename[0:len(filename)-4] != f"wk{weekno}"):
                            extrafiles = fileinfo['extrafiles']
                            title = filename[0:len(filename)-4]
                            fileurl = os.path.join(baseurl, filepath).replace('\\','/')
                            extrafileinfo = {"title": title, "url": fileurl}
                            extrafiles.append(extrafileinfo)
                            fileinfo["extrafiles"] = extrafiles                  
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
                print(f"mdtitle search {line}")
                x = re.search(r"#{2}\s(.*)$", line) ## match markdown title
                if (x is not None):
                    title = x.group(1)
                    if (title != ""):
                        print(f"mdtitle found {title}")
                        return title 
        return ""
    
    def htmlfiletitle(self,filepath):
        with open(filepath, 'r',encoding="utf-8") as infile:
            for line in infile:
                print(f"htmltitle search {line}")
                x = re.search(r"<title>([^<]*)</title>$", line) ## match html title
                if (x is not None):
                    title = x.group(1)
                    if (title != ""):
                        print(f"htmltitle found {title}")
                        return title 
        return ""
    
    def print(self):
        # Walk the files folder.
            for f in self.filesperweek:
                print(f" {f['folder']}/{f['weekno']}")
                #mdtitle
                print(f"-: md: {f['mdtitle']}, html:{f['htmltitle']}")
                print(f"-:  slides:{f['slidesurl']}")
                if (f['pdfslidesurl'] is not None):
                    print(f"-:  slidespdf:{f['pdfslidesurl']}")
                for s in f['extrafiles']:
                    print(f" ->> Extra {s['title']}, {s['url']}")