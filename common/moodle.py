"""
#Created 27/02/2021
@author: andrewdarby

represents sections on moodle website
"""
import pathlib
import os
from os import system, name
from files.script import LocalGetSections

class Moodle():
    def __init__(self):
        # initalise files obj
        self.section = []  # List of current section
        self.sectionsToUpdate = [] # List of sections to update
        
        
    def FetchSections(self,courseId):       
        self.section = LocalGetSections(courseId)
        
    def BuildSectionsToUpdate(self,courseId):       
        self.section = LocalGetSections(courseId)
        
        
        
        course.FetchSections(courseid)
course.FindSectionsToUpdate(files.filesperweek)