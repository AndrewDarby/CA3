from datetime import datetime
import json
from common.files import Files
from common.moodle import Moodle
from common.videos import Videos

GITHUBBASEURL = "https://github.com/AndrewDarby/CA3"
GDRIVEVIDEOFOLDER ="https://drive.google.com/drive/folders/1pFHUrmpLv9gEJsvJYKxMdISuQuQsd_qX"
MOODLEURL = ""
FILESFOLDER = "files/"
ALLFILES = ['.html','.md','.pdf','.ppt']
SECODNDARYFILES = ['.pdf','.ppt']
TERMSTARTDATES = ['01/10/2020','01/01/2021','10/05/2021']
WEEKSPERTERM = 12

courseid = "15"
viewcourse="https://034f8a1dcb5c.eu.ngrok.io/course/view.php?id=15"


# Scan all local folders, and add to dictionary
files = Files()
files.findfiles(FILESFOLDER,GITHUBBASEURL,ALLFILES,SECODNDARYFILES) 
#files.print()

videos = Videos()
videos.findvideos(GDRIVEVIDEOFOLDER,TERMSTARTDATES)

'''
## get current sections on moodle
course = Moodle()
course.FetchSections(courseid)
####course.PrintSections() 
course.BuildSectionsToUpdate(files.filesperweek)
course.PrintUpdateSections()
course.UploadChanges(courseid)
'''

    
    
    # references
    # https://regex101.com/
    # https://docs.python.org/3/howto/regex.html
    # https://stackoverflow.com/questions/16522415/how-to-get-a-capture-group-that-doesnt-always-exist
    #https://stackoverflow.com/questions/72899/how-do-i-sort-a-list-of-dictionaries-by-a-value-of-the-dictionary