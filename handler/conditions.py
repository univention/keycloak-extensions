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

        login_errors = list(utils.filter_events_by_type(self.events, "LOGIN_ERROR"))
        print(self.__class__.__name__, "({})".format(field), "- Login Errors:", len(login_errors))
        timestamp_to_events = utils.build_timestamp_to_event_dict(login_errors)
        times = list(filter(lambda x: x - datetime.datetime.now() < self.timeframe,
                            timestamp_to_events.keys()))

        # check per IP-fails #
        count_map = {}
        field_content_to_any_event = {}
        for t in times:
            # try main structure #
            field_content = timestamp_to_events[t].get(field)

            # try details #
            if not field_content:
                details = timestamp_to_events[t].get("details")
                if details:
                    field_content = details.get(field)

            # continue if still not found #
            if not field_content:
                continue

            if field_content in count_map:
                count_map[field_content] += 1
            else:
                count_map[field_content] = 1
                field_content_to_any_event.update({field_content: timestamp_to_events[t]})

        print(count_map)
        above_values = [x for x in count_map if count_map[x] > self.threshold]
        results = []
        for v in above_values:
            results.append((field_content_to_any_event[v], count_map[v], field))
        return results
