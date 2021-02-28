from datetime import datetime
import json
from common.files import Files
from common.moodle import Moodle
from files.script import LocalGetSections

GITHUBBASEURL = "https://mikhail-cct.github.io/ca3-test"
MOODLEURL = ""
FILESFOLDER = "files/"
ALLFILES = ['.html','.md','.pdf','.ppt']
SECODNDARYFILES = ['.pdf','.ppt']

courseid = "15"
password = "Cct2021#"
viewcourse="https://034f8a1dcb5c.eu.ngrok.io/course/view.php?id=15"


# Scan all local folders, and add to dictionary
files = Files()
files.findfiles(FILESFOLDER,GITHUBBASEURL,ALLFILES,SECODNDARYFILES) 
files.print()

## get current sections on moodle
course = Moodle()
course.FetchSections(courseid)
#course.PrintSections() 
course.BuildSectionsToUpdate(files.filesperweek)
course.PrintUpdateSections()

## Write the data back to Moodle
#sec_write = LocalUpdateSections(courseid, data)

# y
'''
for x in range(1,len(sec.getsections)):
    print(f"number {x}")
    print(json.dumps(sec.getsections[x]['summary'], indent=4, sort_keys=True))
    month = parser.parse(list(sec.getsections)[1]['name'].split('-')[0])
    # Show the resulting timestamp
    print(month)
    # Extract the week number from the start of the calendar year
    print(month.strftime("%V"))
    '''
    
    
    # references
    # https://regex101.com/
    # https://docs.python.org/3/howto/regex.html
    # https://stackoverflow.com/questions/16522415/how-to-get-a-capture-group-that-doesnt-always-exist