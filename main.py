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
TERMSTARTDATES = ['2020-09-28','2021-01-01','2021-05-01']
WEEKSPERTERM = 12

courseid = "15"
viewcourse="https://034f8a1dcb5c.eu.ngrok.io/course/view.php?id=15"

## get current sections on moodle
course = Moodle()
course.FetchSections(courseid)
#course.PrintSections()

# Scan all local folders, and add to dictionary
files = Files()
files.findfiles(FILESFOLDER,GITHUBBASEURL,ALLFILES,SECODNDARYFILES) 
#files.print()

#course.BuildSectionsFromFiles(files.filesperweek)
#course.PrintUpdateSections()
#course.UploadChanges(courseid)

videos = Videos()
videos.findvideos(GDRIVEVIDEOFOLDER,TERMSTARTDATES) ## remember read from live url !!
videos.sortvideosintosections()
videos.printlinks()
videos.printsections()
course.ClearSectionsToUpdate()
course.BuildSectionsFromVideos(videos.videospersection)


#course.BuildSectionsFromFiles(files.filesperweek)
course.PrintUpdateSections()
course.UploadChanges(courseid)

    
    
    # references
    # https://regex101.com/
    # https://docs.python.org/3/howto/regex.html
    # https://stackoverflow.com/questions/16522415/how-to-get-a-capture-group-that-doesnt-always-exist
    #https://stackoverflow.com/questions/72899/how-do-i-sort-a-list-of-dictionaries-by-a-value-of-the-dictionary