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
    "learning": [],
    "coding": [],

    "work": [],
    "co-op": [],
    "school": [],
    "workout": [],
    "mentoring": [],
    "bookmarks": [],
    "intrinsic building": [],

    "body": [],
    "soul": [],

    "errands": [],
    "transition": [],
    "break": [],
    "wandering": [],
    "procrastination": [],

    # Specific
    "health": [],
    "healthcare": [],
    "cells": [],
    "podcast": [],
    "yc": [],
    "music": [],
}

otherCategories = {
    "cs349": "school",
    "cs 349": "school",
    "cs341": "school",
    "cs 341": "school",
    "se350": "school",
    "se 350": "school",
    "math213": "school",
    "math 213": "school",
    "se465": "school",
    "se 465": "school",
    "econ101": "school",
    "econ 101": "school",
    "che161": "school",
    "che 161": "school",
}

# Set initial times for each day, for each category to zero
for category in categories.keys():
    categories[category] = [0] * len(dates)

pageCount = 0
skippedTags = []

for page in allPages:
    pageTitle = page.get("title")

    try:
        # Filter out daily pages
        dailyPage = parse(pageTitle)
        dailyPage = dailyPage.date()

        # Filter time range selected
        if dailyPage >= startTermDate and dailyPage <= endTermDate:
            dateIndex = next((i for i, item in enumerate(dates) if item == dailyPage), -1)

            notes = page.get("children")
            if notes is not None:
                for note in notes:
                    # Get time boxes
                    parentTitle = note.get("string")

                    # If time tracking parent note and if end time exists
                    timeBlock = parseTimeBlock(parentTitle)
                    if timeBlock != None:
                        taskMinutes = getTimeDelta(timeBlock[0], timeBlock[1])

                        task = parentTitle[parentTitle.index(timeBlock[1])+6:]
                        task = task.lower().lstrip().rstrip()

                        if task != None:
                            # Check if task is in category list
                            category = [key for key, value in categories.items() if key.lower() in task]
                            if len(category) != 1:
                                # IF it's not in the list, check other special category list, which maps to a category
                                category = [value for key, value in otherCategories.items() if key.lower() in task]
                                if len(category) != 1:
                                    skippedTags.append({"title": page.get("title"), "tag": task})
                                    continue
                            category = category[0]

                            # # Append category time to category list of times
                            categoryTimes = categories.get(category)
                            categoryTimes[dateIndex] += taskMinutes

            pageCount += 1

    except:
        continue

print("-"*10)
print("Analyzed: " + str(pageCount) + " pages")
print("Skipped Tasks: ", len(skippedTags))
for skippedTag in skippedTags:
    print("FIX TAG: ")
    print("-"*10)
    print(skippedTag["title"])
    print(skippedTag["tag"])
    print("-"*10)
print("-"*10)

percentTimes = []
for category, categoryTimes in categories.items():
    totalActivityMinutes = sum(categoryTimes)
    percentTimes.append({"category": category, "percentTime": round((totalActivityMinutes/totalMinutes)*100, 2)})

percentTimes.sort(key=lambda x: x.get("percentTime"), reverse=True)

print("Percent Time Breakdown Per Activity: ")
print("-"*10)
for percentTime in percentTimes:
    print(percentTime.get("category")  + " (" + str(percentTime.get("percentTime")) + "%)")
print("-"*10)

# dateLabels = [x.strftime("%b %d") for x in dates]
# figure(figsize=(17, 7))

# ax = plt.axes()
# ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
# ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))

# plt.xticks(rotation=45, fontsize=10)
# plt.plot(dateLabels, categories.get("reading"),  color='red', label='reading')
# plt.plot(dateLabels, categories.get("school"),  color='blue', label='school')
# plt.legend()
# plt.title('Minutes spent on activity per day')
# plt.xlabel('Day')
# plt.ylabel('Time (minutes)')
# plt.show()
