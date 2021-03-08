from datetime import datetime
from common.files import Files
from common.moodle import Moodle
from common.videos import Videos

GITHUBBASEURL = "https://andrewdarby.github.io/CA3"
GDRIVEVIDEOFOLDER ="https://drive.google.com/drive/folders/1pFHUrmpLv9gEJsvJYKxMdISuQuQsd_qX"
FILESFOLDER = "files/"
ALLFILES = ['.html','.md','.pdf','.ppt','.csv','.txt','.py','.ipynb']
SECODNDARYFILES = ['.pdf','.ppt','.csv','.txt','.py','.ipynb']
TERMSTARTDATES = ['2020-09-28','2021-01-01','2021-05-01']

courseid = "15"

## get current sections on moodle
course = Moodle()
course.FetchSections(courseid)
###course.PrintSections()

## NOTE:
## You can run together functions to 'findfiles' and 'findvideos' or run independently
## For example comment out lines #25 - #28, or comment out #31 - #38

##Scan all local folders, and add to dictionary
files = Files()
files.findfiles(FILESFOLDER,GITHUBBASEURL,ALLFILES,SECODNDARYFILES,TERMSTARTDATES) 
course.BuildSectionsFromFiles(files.filesPerSecton)
course.UploadChanges(courseid)

##Scan all local folders, and add to dictionary
videos = Videos()
videos.findvideos(GDRIVEVIDEOFOLDER,TERMSTARTDATES) ## remember read from live url !!
videos.sortvideosintosections()
#videos.printlinks()
#videos.printsections()
course.ClearSectionsToUpdate()
course.BuildSectionsFromVideos(videos.videospersection,TERMSTARTDATES[0])
course.UploadChanges(courseid)

