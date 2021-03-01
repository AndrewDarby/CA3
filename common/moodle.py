"""
#Created 27/02/2021
@author: andrewdarby

represents sections on moodle website
"""
import pathlib
import operator
import os
from os import system, name
from files.script import LocalGetSections, LocalUpdateSections

DOCICON = "<img style=\"margin: 0 6px 6px 0\" src=\"https://034f8a1dcb5c.eu.ngrok.io/theme/image.php/boost/url/1613693725/icon\" class=\"iconlarge activityicon\" alt=\"\" role=\"presentation\" aria-hidden=\"true\">"
PDFICON ="<img style=\"margin: 0 6px 6px 0\" src=\"https://034f8a1dcb5c.eu.ngrok.io/theme/image.php/boost/core/1613693725/f/pdf-24\" class=\"iconlarge activityicon\" alt=\"\" role=\"presentation\" aria-hidden=\"true\">"


class Moodle():
    def __init__(self):
        # initalise files obj
        self.sections = []  # List of current section
        self.sectionsToUpdate = [] # List of sections to update
        
        
    def FetchSections(self,courseId):       
        self.sections = LocalGetSections(courseId)
        
    def BuildSectionsToUpdate(self,files):  
        for f in files:
            sectionId = int(f['weekno'])
            section = self.sections.getsections[sectionId]['summary']
            if (section == ""): # insert new summary HTML
                sectionHTML = self.buildSummaryHTML(f)
            else: # section exists, append to summary
                #sectionHTML = self.appendSummaryHTML(section,f)
                sectionHTML = self.buildSummaryHTML(f)
            sectionInfo = {"summary": sectionHTML, "section": sectionId }
            self.sectionsToUpdate.append(sectionInfo)
        
    def UploadChanges(self,courseId):
        #LocalUpdateSections(courseid, data)
        sec_write = LocalUpdateSections(courseId, self.sectionsToUpdate)
        if (courseId == 0):
            print("nothing here")
     
    def PrintSections(self):  
        for x in range(1,len(self.sections.getsections)):
            sec = self.sections.getsections[x]
            print(f"section {x}")
            print(" - summary",sec['summary'])
            print(" - name",sec['name'])
            
    def PrintUpdateSections(self):  
        for sec in self.sectionsToUpdate:
            print("update section:",sec['section'])
            print(" - summary",sec['summary'])
                     
    def buildSummaryHTML(self,file):
        #set title
        defaulttitle = "Lecture notes: Week {wk_no}".format(wk_no=file['weekno'])
        htmlextra = ""
        
        primaryfolder = "wk{number}".format(number=file['weekno'])
        primaryslides = list(filter(lambda d: d['folder'] in [primaryfolder], file['lectureslides']))
        remainderslides = list(filter(lambda d: d['folder'] not in [primaryfolder], file['lectureslides']))
        lectureslidesSorted = sorted(remainderslides, key=operator.itemgetter('folder'))
        
        #Add primary slides 'wkX'
        htmlslides = self.slideSummaryHTML(defaulttitle,primaryslides[0])
        # Add remainer slides 'wkA, wkC'
        for slide in lectureslidesSorted:     
            foldername = slide['folder']
            defaulttitle = "Lecture notes: Week {wk_no} - {folder}".format(wk_no=file['weekno'],folder=foldername) 
            htmlslides  += "\n" + self.slideSummaryHTML(defaulttitle,slide)                      
     
        #Add any extra non slides pdf or ppt
        if (("extrafiles" in file) and file["extrafiles"] != ""):
            for s in file["extrafiles"]:
                if (("title" in s) and ("url" in s)):
                    htmlextra += "\n<p style=\"margin:10px 0 10px 25px\"><a href=\"{url}\">{icon}<span>{title}</span></a></p>".format(url=s['url'], icon=DOCICON, title=s['title'])
                    
        return htmlslides + htmlextra 
    
    def slideSummaryHTML(self,title,slide):
        if (("mdtitle" in slide) and (slide['mdtitle'] != "")):
            title = slide['mdtitle']
        elif (("htmltitle" in slide) and slide['htmltitle'] != ""):
            title = slide['htmltitle']
        #Add link to slides + pdf
        html = "<a href=\"{url}\">{icon}<span>{title}</span></a>".format(url=slide['slidesurl'], icon=DOCICON,title=title)
        if ("pdfslidesurl" in slide and slide["pdfslidesurl"] != ""):
            html += "\n  <a style=\"margin-left:15px\" href=\"{url}\">{icon}<span>{title} (pdf)</span></a><br>".format(url=slide['pdfslidesurl'], icon=PDFICON,title=title)  
        return html          
        