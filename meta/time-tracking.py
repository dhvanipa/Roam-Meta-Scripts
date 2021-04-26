import json
from datetime import timedelta
from dateutil.parser import parse

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import matplotlib.ticker as ticker

from helper import parseTimeBlock, getTimeDelta, getTimeStr, getTimeRange

# Load Roam graph
with open('../data/database.json') as f:
    allPages = json.load(f)

# Setup
(chosenYear, chosenTrimester, chosenTrimesterName, startTermDate, endTermDate) = getTimeRange()

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
    "event": [],

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
    "bio": [],
    "cybersecurity": [],
    "power": [],
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
                        if ' - ' in task:
                            task = task[:task.index(' - ')]

                        if task != None:
                            # Check if task is in category list
                            category = [key for key, value in categories.items() if key.lower() in task]
                            if len(category) == 0:
                                # IF it's not in the list, check other special category list, which maps to a category
                                category = [value for key, value in otherCategories.items() if key.lower() in task]
                                if len(category) != 1:
                                    skippedTags.append({"title": page.get("title"), "tag": task, "category": category})
                                    continue
                            elif len(category) > 1:
                                # pick the longest substring
                                category = [max(category, key=len)]

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
    print(skippedTag["category"])
    print("-"*10)
print("-"*10)

untrackedMinutes = totalMinutes
percentTimes = []
for category, categoryTimes in categories.items():
    totalActivityMinutes = sum(categoryTimes)
    untrackedMinutes -= totalActivityMinutes
    nonZeroTimes = [x for x in categoryTimes if x > 0]
    averageMinutes = 0
    if len(nonZeroTimes) > 0:
        averageMinutes = round(sum(nonZeroTimes)/len(nonZeroTimes))

    percentTimes.append({
        "category": category,
        "percentTime": round((totalActivityMinutes/totalMinutes)*100, 2),
        "totalMins": getTimeStr(totalActivityMinutes),
        "avgMins": getTimeStr(averageMinutes)
        })


percentTimes.sort(key=lambda x: x.get("percentTime"), reverse=True)

print("Time Breakdown Per Activity: ")
print("-"*10)
print("untracked ({0}%)".format(round((untrackedMinutes/totalMinutes)*100, 2)))
for percentTime in percentTimes:
    print("{0} ({1}%), Total: {2}, Avg: {3}".format(
        percentTime.get("category"),
        percentTime.get("percentTime"),
        percentTime.get("totalMins"),
        percentTime.get("avgMins")
        ))
print("-"*10)


print("Interactive Grapher")
print("-"*10)
while True:
    # Let user pick an activity to graph
    chosenActivity = input("Enter activity from list to graph (or exit): ")
    while chosenActivity not in categories.keys() and chosenActivity != "exit":
        print("Invalid activity chosen")
        chosenActivity = input("Enter activity from list to graph (or exit): ")

    if chosenActivity == "exit":
        break

    dateLabels = [x.strftime("%b %d") for x in dates]
    figure(figsize=(17, 7))

    ax = plt.axes()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))

    plt.xticks(rotation=45, fontsize=10)
    plt.plot(dateLabels, categories.get(chosenActivity),  color='blue', label=chosenActivity)
    plt.legend()
    plt.title('Minutes spent on {0} per day during {1} of {2}'.format(chosenActivity, chosenTrimesterName, chosenYear))
    plt.xlabel('Day')
    plt.ylabel('Time (minutes)')
    plt.draw()
    plt.pause(1)
    prevChosenActivity = chosenActivity
    chosenActivity = input("Enter other activity from list to graph for comparison (or skip): ")
    while chosenActivity not in categories.keys() and chosenActivity != "skip":
        print("Invalid comparison activity chosen")
        chosenActivity = input("Enter other activity from list to graph for comparison (or skip): ")

    if chosenActivity == "skip":
        continue

    plt.title('Minutes spent on {0} vs. {1} per day during {2} of {3}'.format(
        prevChosenActivity, chosenActivity, chosenTrimesterName, chosenYear))
    plt.plot(dateLabels, categories.get(chosenActivity),  color='red', label=chosenActivity)
    plt.legend()
    plt.draw()
    plt.pause(1)