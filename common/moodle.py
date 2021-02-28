"""
#Created 27/02/2021
@author: andrewdarby

represents sections on moodle website
"""
import pathlib
import os
from os import system, name
from files.script import LocalGetSections, LocalUpdateSections

PDFICON = "<img src=\"/files/pdf-24.png\" aria-hidden=\"true\">"
DOCICON = "<img src=\"/files/icon.svg\" aria-hidden=\"true\">"


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
        
    def UploadChanges(self,courseID):
        #LocalUpdateSections(courseid, data)
        nop
     
    def PrintSections(self):  
        for x in range(1,len(self.sections.getsections)):
            sec = self.sections.getsections[x]
            print(f"section {x}")
            print(" - summary",sec['summary'])
            print(" - name",sec['name'])
            
    def PrintUpdateSections(self):  
        for sec in range(1,len(self.sectionsToUpdate)):
            print("update section:",sec['section'])
            print(" - summary",sec['summary'])
                     
    def buildSummaryHTML(self,file):
        #set title
        title = "Lecture notes: Week {wk_no}".format(wk_no=file['weekno'])
        if (("mdtitle" in file) and (file['mdtitle'] != "")):
            title = file['mdtitle']
        elif (("htmltitle" in file) and file['htmltitle'] != ""):
            title = file['htmltitle']
        
        #Add link to slides + pdf
        html = "<a href=\"{url}\">{icon}<span>{title}</span></a><br>".format(url=file['slidesurl'], icon=DOCICON,title=title)
        if ("pdfslidesurl" in file and file["pdfslidesurl"] != ""):
            html += "<a href=\"{url}\">{icon}<span>{title} (pdf)</span></a><br>".format(url=file['pdfslidesurl'], icon=PDFICON,title=title)
        #Add slides to any extra non primary pdf or ppt
        if (("extrafiles" in file) and file["extrafiles"] != ""):
            for s in file["extrafiles"]:
                if (("title" in s) and ("url" in s)):
                    html += "<p><a href=\"{url}\">{icon}<span>{title}</span></a></p>".format(url=file['url'], icon=DOCICON, title=s['title'])
                        
        