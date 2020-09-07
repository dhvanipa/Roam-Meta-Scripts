import json
import re
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt


with open('data/database.json') as f:
  allPages = json.load(f)

summerTerm = ("May", "June", "July", "August")

timeRange = summerTerm
year = "2020"
    
hhmmStartsWithCheck = re.compile("^([0-1]?[0-9]|2[0-3]):[0-5][0-9]")
hhmmStrictCheck = re.compile("^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$")

dates = ["Jan 1", "Jan 2"]
timeSpent = [3, 4]

categories = [
    "thinking",    
    "transition",    
    "wandering",
    "procrastination",    
    "workout",
    "family",
    "friends",
    "lunch",
    "dinner",
    "morning routine",                               
    "info consumption",
    "research",
    "errands",
    "planning",
    "reflecting",   
    "break",
    "school",    
    "coding",
    "walk",
    "reading",
    "yc",
    "co-op",    
    "bookmark",
    "wandcrafting", 
    "reflection",
]

categoriesRaw = [
    "thinking",
    "think",
    "transition",    
    "wandering",
    "procrastination",
    "work out",
    "workout",
    "family",
    "friends",
    "lunch",
    "dinner",
    "morning exercise.",
    "morning exercise. shower. get ready",
    "shower. get ready",
    "shower. morning exercise.",
    "shower and get ready.",    
    "get ready",
    "morning exercise. shower.",    
    "setup",
    "info consumption",
    "research",
    "errands",
    "planning",
    "reflecting",
    "cs348",
    "cs 348",
    "cs240",
    "cs 240",
    "cs370",
    "cs 370",
    "cs247",
    "cs 247",
    "math239",
    "math 239",
    "ece192",
    "ece 192",
    "break",
    "school",    
    "coding",
    "walk",
    "reading",
    "yc",
    "co-op",
    "coop",
    "bookmark",
    "wandcrafting",
    "wandservers",    
    "reflection",
]

pageCount = 0

for page in allPages:    
    pageTitle = page.get("title")

    # Filter out daily pages
    if pageTitle.startswith(timeRange) and pageTitle.endswith(year):
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

                        task = parentTitle[endTimeStartIndex+5:]                        
                        task = task.lower()                        

                        if not any(map(task.__contains__, categoriesRaw)):
                            print("FIX TAG: ")
                            print(page.get("title"))   
                            print(task)
                        else:
                            for rawCat in categoriesRaw:
                                if rawCat.find(task):
                                    print(rawCat)                        

                            # print(tdelta)
                            # hours = tdelta.seconds//3600 
                            # minutes = (td.seconds//60)%60                       
                      
                        # break            
    
            pageCount += 1
        
        # break

print("-----------")
print("Analyzed: " + str(pageCount) + " pages")

plt.plot(dates, timeSpent)
plt.title('Minutes spent per day')
plt.xlabel('Day')
plt.ylabel('Time (minutes)')
plt.show()