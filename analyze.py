import json
import re
from datetime import datetime
from datetime import timedelta

with open('data/database.json') as f:
  allPages = json.load(f)

summer_term = ("May", "June", "July", "August")

time_range = summer_term
year = "2020"
    
hhmmStartsWithCheck = re.compile("^([0-1]?[0-9]|2[0-3]):[0-5][0-9]")
hhmmStrictCheck = re.compile("^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$")

page_count = 0
for page in allPages:    
    pageTitle = page.get("title")

    # Filter out daily pages
    if pageTitle.startswith(time_range) and pageTitle.endswith(year):
        # print(page.get("title"))   
        notes = page.get("children")

        # If page isn't empty
        if notes is not None:
            for note in notes:
                # Get time boxes
                parentTitle = note.get("string")
                
                # If time tracking parent note
                if hhmmStartsWithCheck.match(parentTitle):
                    # If end time exists                    
                    endTimeStartIndex = re.search(r"\d", parentTitle[5:])
                    if endTimeStartIndex is not None:                        
                        # print(parentTitle)
                        
                        startTime = parentTitle[0:5]
                        assert(hhmmStrictCheck.match(startTime))

                        # print(startTime)           
                        
                        endTimeStartIndex = endTimeStartIndex.start() + 5
                        endTime = parentTitle[endTimeStartIndex:endTimeStartIndex+5]
                        assert(hhmmStrictCheck.match(endTime))

                        # print(endTime)           

                        FMT = '%H:%M'
                        tdelta = datetime.strptime(endTime, FMT) - datetime.strptime(startTime, FMT)       
                        if tdelta.days < 0:
                            tdelta = timedelta(days=0, seconds=tdelta.seconds, microseconds=tdelta.microseconds)

                        # print(tdelta)
                        # hours = tdelta.seconds//3600 
                        # minutes = (td.seconds//60)%60                       
                      
                        # break            
    
            page_count += 1
        
        # break

print("-----------")
print("Analyzed: " + str(page_count) + " pages")