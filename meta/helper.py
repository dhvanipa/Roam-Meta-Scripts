import re
from datetime import datetime, timedelta

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

# Gets the time delta between start and end time in seconds
# eg. startTime: 13:36, endTime: 14:36
# return: 3600
def getTimeDelta(startTime, endTime):
    FMT = '%H:%M'
    tdelta = datetime.strptime(
        endTime, FMT) - datetime.strptime(startTime, FMT)
    if tdelta.days < 0:
        tdelta = timedelta(days=0, seconds=tdelta.seconds, microseconds=tdelta.microseconds)
    return tdelta