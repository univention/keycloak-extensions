import datetime


def parseEventDate(e):
    timeInJson = int(e["time"])  # careful this is unix in ms
    timeParsed = datetime.datetime.fromtimestamp(timeInJson // 1000)
    e["time"] = timeParsed
    return e


def buildTimestampToEventDict(events):
    timeEventDict = dict()
    for e in events:
        timeEventDict.update({e["time"]: e})
    return timeEventDict


def filterEventsByType(events, typeString):
    if not typeString:
        return events
    return filter(lambda e: e["type"] == typeString, events)


def filterOutTokenErrors(events, field, notValue):
    return filter(lambda e: e.get("details").get(field) != notValue, events)
