import utils
import datetime


class Condition:

    def __init__(self, events, threshold, timeframe):
        self.events = events
        self.threshold = threshold
        self.timeframe = timeframe

    def check(**kwargs):
        raise NotImplementedError()


class ConditionFieldSpecificLimit(Condition):

    def check(self, **kwargs):

        field = kwargs["field"]

        login_errors = list(utils.filterEventsByType(self.events, "LOGIN_ERROR"))
        print(self.__class__.__name__, "({})".format(field), "- Login Errors:", len(login_errors))
        timestampToEvents = utils.buildTimestampToEventDict(login_errors)
        times = list(filter(lambda x: x - datetime.datetime.now() < self.timeframe,
                            timestampToEvents.keys()))

        # check per IP-fails #
        countMap = {}
        fieldContentToAnyEvent = {}
        for t in times:

            # try main structure #
            fieldContent = timestampToEvents[t].get(field)

            # try details #
            if not fieldContent:
                details = timestampToEvents[t].get("details")
                if details:
                    fieldContent = details.get(field)

            # continue if still not found #
            if not fieldContent:
                continue

            if fieldContent in countMap:
                countMap[fieldContent] += 1
            else:
                countMap[fieldContent] = 1
                fieldContentToAnyEvent.update({fieldContent: timestampToEvents[t]})

        print(countMap)
        aboveValues = list(filter(lambda x: countMap[x] > self.threshold, countMap.keys()))
        results = []
        for v in aboveValues:
            results.append((fieldContentToAnyEvent[v], countMap[v], field))
        return results
