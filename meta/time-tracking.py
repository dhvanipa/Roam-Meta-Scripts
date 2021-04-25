import json
from datetime import date, datetime, timedelta
from calendar import month_abbr, monthrange
from dateutil.parser import parse

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import matplotlib.ticker as ticker

from helper import parseTimeBlock, getTimeDelta

# Load Roam graph
with open('../data/database.json') as f:
    allPages = json.load(f)

# Setup

# Map month to number of days
months = {month: index for index, month in enumerate(month_abbr) if month}

# Start - End months
winterTerm = ("Jan", "Apr")
springTerm = ("May", "Aug")
fallTerm = ("Sep", "Dec")

year = {"2020": 2020, "2021": 2021}
trimesters = {"winter": winterTerm, "spring": springTerm, "fall": fallTerm}

# Get input
chosenYear = input("Enter year (2020, 2021): ")
while chosenYear not in year:
    print("Invalid year chosen")
    chosenYear = input("Enter year (2020, 2021): ")

chosenTrimester = input("Enter trimester (winter, spring, fall): ")
while chosenTrimester not in trimesters:
    print("Invalid trimester chosen")
    chosenTrimester = input("Enter trimester (winter, spring, fall): ")
chosenTrimester = trimesters.get(chosenTrimester)

startTermDate = date(
    int(chosenYear),
    months.get(chosenTrimester[0]),
    1)

endTermDate = date(
    int(chosenYear),
    months.get(chosenTrimester[1]),
    monthrange(int(chosenYear), months.get(chosenTrimester[1]))[1])

# Get list of dates
dates = [startTermDate + timedelta(days=x) for x in range((endTermDate-startTermDate).days + 1)]
totalMinutes = len(dates) * (24*60)

categories = {
    # General
    "family": [],
    "friends": [],

    "morning routine": [],
    "lunch": [],
    "dinner": [],

    "thinking": [],
    "reflecting": [],
    "planning": [],
    "reading": [],
    "writing": [],
    "coding": [],

    "work": [],
    "co-op": [],
    "school": [],
    "workout": [],
    "bookmarks": [],

    "errands": [],
    "transition": [],
    "break": [],
    "wandering": [],
    "procrastination": [],

    # Specific
    "healthcare": [],
}

otherCategoriesRaw = {
    "cs349": "school",
    "cs341": "school",
    "se350": "school",
    "math213": "school",
    "se465": "school",
    "econ101": "school",
    "che161": "school",
}

pageCount = 0

for page in allPages:
    pageTitle = page.get("title")

    try:
        # Filter out daily pages
        dailyPage = parse(pageTitle)
        dailyPage = dailyPage.date()

        # Filter time range selected
        if dailyPage >= startTermDate and dailyPage <= endTermDate:
            notes = page.get("children")
            if notes is not None:
                for note in notes:
                    # Get time boxes
                    parentTitle = note.get("string")

                    # If time tracking parent note and if end time exists
                    timeBlock = parseTimeBlock(parentTitle)
                    if timeBlock != None:
                        tdelta = getTimeDelta(timeBlock[0], timeBlock[1])

                        task = parentTitle[parentTitle.index(timeBlock[1])+6:]
                        task = task.lower().lstrip().rstrip()

            pageCount += 1

    except:
        continue


# if not any(map(task.__contains__, categoriesRaw)):
#                             print("FIX TAG: ")
#                             print(page.get("title"))
#                             print(task)
#                         else:
#                             category = ""
#                             for rawCat in categoriesRaw:
#                                 if task.find(rawCat) > 0:
#                                     category = rawCat
#                                     break

#                             # Calculate reading
#                             # print(category)
#                             if category == "reflecting":
#                                 # print(pageTitle)

#                                 # print(tdelta)
#                                 hours = tdelta.seconds//3600
#                                 minutes = (tdelta.seconds//60) % 60
#                                 taskMinutes = (hours*60) + minutes

#                                 timeSpent[termIndex] += taskMinutes
#                                 # print(timeSpent[termIndex])
#                                 activityMinutes += taskMinutes

# print("-----------")
# print("Analyzed: " + str(pageCount) + " pages")
# print("Activity: lunch")
# print("Average time (minutes): " + str(activityMinutes) + "/" +
#       str(totalMinutes) + " (" + str(round((activityMinutes/totalMinutes)*100, 2)) + "%)")

# figure(figsize=(17, 7))

# ax = plt.axes()
# ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
# ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))

# plt.xticks(rotation=45, fontsize=10)
# plt.plot(dates, timeSpent)
# plt.title('Minutes spent reflecting per day')
# plt.xlabel('Day')
# plt.ylabel('Time (minutes)')
# plt.show()
