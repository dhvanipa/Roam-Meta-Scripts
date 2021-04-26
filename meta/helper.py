import re
from datetime import date, datetime, timedelta
from calendar import month_abbr, monthrange
from math import floor

hhmmStartsWithCheck = re.compile("^([0-1]?[0-9]|2[0-3]):[0-5][0-9]")
hhmmStrictCheck = re.compile("^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$")

# Parses a string with a time block to a tuple with the start and end time
# eg. timeStr: 13:36 - 14:46: Reading
# return: (13:36, 14:46)
def parseTimeBlock(timeStr):
    if hhmmStartsWithCheck.match(timeStr):
        endTimeStartIndex = re.search(r"\d", timeStr[5:])
        if endTimeStartIndex is not None:
            startTime = timeStr[0:5]
            assert(hhmmStrictCheck.match(startTime))

            endTimeStartIndex = endTimeStartIndex.start() + 5
            endTime = timeStr[endTimeStartIndex:endTimeStartIndex+5]
            assert(hhmmStrictCheck.match(endTime))

            return (startTime, endTime)
    return None

# Gets the time delta between start and end time in minutes
# eg. startTime: 13:36, endTime: 14:36
# return: 60
def getTimeDelta(startTime, endTime):
    FMT = '%H:%M'
    tdelta = datetime.strptime(
        endTime, FMT) - datetime.strptime(startTime, FMT)
    if tdelta.days < 0:
        tdelta = timedelta(days=0, seconds=tdelta.seconds, microseconds=tdelta.microseconds)

    # convert seconds to minutes
    hours = tdelta.seconds//3600
    minutes = (tdelta.seconds//60) % 60
    taskMinutes = (hours*60) + minutes

    return taskMinutes

# Takes in an integer represent the number of minutes and returns a user friendly string
# eg. minutes: 344
# return: 5 hours and 44 minutes
def getTimeStr(minutes):
    time = ""
    if minutes > 60:
        hours = floor(minutes/60)
        if hours == 1:
            time = str(hours) + " hour and "
        else:
            time = str(hours) + " hours and "
        minutes = minutes % 60

    if minutes == 1:
        time += str(minutes) + " min"
    else:
        time += str(minutes) + " mins"

    return time

# Get's a time range from the user and returns a tuple of:
# return (chosenYear, chosenTrimester, chosenTrimesterName, startDateTime, endDateTime)
def getTimeRange():
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
    chosenTrimesterName = chosenTrimester.capitalize()
    chosenTrimester = trimesters.get(chosenTrimester)

    startTermDate = date(
        int(chosenYear),
        months.get(chosenTrimester[0]),
        1)

    endTermDate = date(
        int(chosenYear),
        months.get(chosenTrimester[1]),
        monthrange(int(chosenYear), months.get(chosenTrimester[1]))[1])

    return (chosenYear, chosenTrimester, chosenTrimesterName, startTermDate, endTermDate)
