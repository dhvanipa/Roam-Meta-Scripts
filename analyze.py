import json
import re
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import matplotlib.ticker as ticker

# Map month to number of days
monthDays = {"January": 31, "February": 29, "March": 31,
             "April": 30, "May": 31, "June": 30, "July": 31,
             "August": 31, "September": 30, "October": 31,
             "November": 30, "December": 31}

with open('data/database.json') as f:
    allPages = json.load(f)

summerTerm = ("May", "June", "July", "August")
summerTermIndexes = [0, 31, 61, 92]

timeRange = summerTerm
timeRangeIndexes = summerTermIndexes

year = "2020"

hhmmStartsWithCheck = re.compile("^([0-1]?[0-9]|2[0-3]):[0-5][0-9]")
hhmmStrictCheck = re.compile("^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$")

dates = []

# In minutes
timeSpent = []
totalMinutes = 0

for month in timeRange:
    numDays = monthDays.get(month)
    for day in range(1, numDays+1):
        dates.append(month + str(day))
        timeSpent.append(0)
        totalMinutes += (24*60)

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

activityMinutes = 0

for page in allPages:
    pageTitle = page.get("title")

    # Filter out daily pages
    if pageTitle.startswith(timeRange) and pageTitle.endswith(year):
        # print(page.get("title"))
        notes = page.get("children")
        pageMonth = pageTitle[:pageTitle.find(" ")]
        pageDay = int(pageTitle[pageTitle.find(" ")+1:pageTitle.find(",")-2])
        termIndex = timeRangeIndexes[summerTerm.index(pageMonth)] + pageDay - 1

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
                        tdelta = datetime.strptime(
                            endTime, FMT) - datetime.strptime(startTime, FMT)
                        if tdelta.days < 0:
                            tdelta = timedelta(
                                days=0, seconds=tdelta.seconds, microseconds=tdelta.microseconds)

                        task = parentTitle[endTimeStartIndex+5:]
                        task = task.lower()

                        if not any(map(task.__contains__, categoriesRaw)):
                            print("FIX TAG: ")
                            print(page.get("title"))
                            print(task)
                        else:
                            category = ""
                            for rawCat in categoriesRaw:
                                if task.find(rawCat) > 0:
                                    category = rawCat
                                    break

                            # Calculate reading
                            # print(category)
                            if category == "reading":
                                # print(pageTitle)

                                # print(tdelta)
                                hours = tdelta.seconds//3600
                                minutes = (tdelta.seconds//60) % 60
                                taskMinutes = (hours*60) + minutes

                                timeSpent[termIndex] += taskMinutes
                                # print(timeSpent[termIndex])
                                activityMinutes += taskMinutes

                        # break

            pageCount += 1

        # break

print("-----------")
print("Analyzed: " + str(pageCount) + " pages")
print("Activity: reading")
print("Average time (minutes): " + str(activityMinutes) + "/" +
      str(totalMinutes) + " (" + str(round((activityMinutes/totalMinutes)*100, 2)) + "%)")

figure(figsize=(17, 7))

ax = plt.axes()
ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))

plt.xticks(rotation=45, fontsize=10)
plt.plot(dates, timeSpent)
plt.title('Minutes spent per day')
plt.xlabel('Day')
plt.ylabel('Time (minutes)')
plt.show()
