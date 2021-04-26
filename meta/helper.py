import re
from datetime import datetime, timedelta
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