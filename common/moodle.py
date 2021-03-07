"""
#Created 27/02/2021
@author: andrewdarby

represents sections on moodle website
"""
import pathlib
import datetime
from os import system, name
from urllib.parse import urlparse
from files.script import LocalGetSections, LocalUpdateSections
from common.webbuilder import buildFilesSummary, buildVideoSummary, findActionsByClass

MOODLESECTION = {'type': 'num', 'section': 0, 'summary': '', 'summaryformat': 1, 'visible': 1 , 'highlight': 0, 'sectionformatoptions': [{'name': 'level', 'value': '1'}]}
            

class Moodle():
    def __init__(self):
        # initalise files obj
        self.sections = []  # List of current section
        self.sectionsToUpdate = [] # List of sections to update
        
        
    def FetchSections(self,courseId):       
        self.sections = LocalGetSections(courseId)
            
        
    def GetSectionDateTitle(self,sectionid,yearstart):
        yearstart = datetime.datetime.strptime(yearstart, '%Y-%m-%d')
        sectionstartdate = yearstart + datetime.timedelta(days=(sectionid-1)*7)
        sectionenddate = sectionstartdate + datetime.timedelta(days=6)
        title = "{startdate} - {enddate}".format(startdate =sectionstartdate.strftime("%d %B"),enddate = sectionenddate.strftime("%d %B"))
        return title
        
    def ClearSectionsToUpdate(self):
        self.sectionsToUpdate = [] 
        
    # Build html for Files/slides:
    def BuildSectionsFromFiles(self,filesections): 
        sections = filesections.values()
        for f in sections: 
            sectionid = int(f['sectionid'])
            section = self.sections.getsections[sectionid]['summary']
            if (section == ""): # insert new summary HTML
                sectionHTML = buildFilesSummary(f)
            else: # section exists
                #Grap video links, and rebuild-all-files
                videoHTML = findActionsByClass(section,"video")
                sectionHTML = videoHTML + buildFilesSummary(f)
            sectionInfo = MOODLESECTION.copy()
            sectionInfo['section'] = sectionid
            sectionInfo['summary'] = sectionHTML

            ##sectionInfo = {"summary": sectionHTML, "section": sectionId }  # REMOVE 
            self.sectionsToUpdate.append(sectionInfo)
            
    # Build html for Videos:
    # note different video in list can match same section#
    def BuildSectionsFromVideos(self,videosbysection,yearstart):
        for sectionid in videosbysection:
            videos = videosbysection[sectionid]['videolinks']
            videoHTML = ""
            for v in videos:
                videoHTML += buildVideoSummary(v)
            section = self.sections.getsections[sectionid]['summary'] #exiting moodle sections
            if (section == ""): # insert new summary HTML
                sectionHTML = videoHTML
            else: # section exists
                #Grap video links, and rebuild-all-files
                slidesHTML = findActionsByClass(section,"slides")
                filesHTML = findActionsByClass(section,"files")
                sectionHTML =  videoHTML + slidesHTML + filesHTML
            sectionInfo = MOODLESECTION.copy()
            sectionInfo['section'] = sectionid
            sectionInfo['summary'] = sectionHTML
            sectionname = self.sections.getsections[sectionid]['name']
            if ('Topic' in sectionname):
                newname = self.GetSectionDateTitle(sectionid,yearstart)
                sectionInfo['name'] = newname
            self.sectionsToUpdate.append(sectionInfo)
        
    def UploadChanges(self,courseId):  
        sec_write = LocalUpdateSections(courseId, self.sectionsToUpdate)
     
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
                     

    