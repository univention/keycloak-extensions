import os
import utils
import datetime
import logging


class Condition:

    def __init__(self, threshold, timeframe):

        # Configure logging
        log_level = os.environ.get('LOG_LEVEL', 'INFO')
        logging.basicConfig(
            format='%(asctime)s %(levelname)s %(message)s',
            datefmt='%d/%m/%Y %I:%M:%S',
            level=log_level)
        self.logger = logging.getLogger(__name__)

        self.threshold = threshold
        self.timeframe = timeframe

    def check(**kwargs):
        raise NotImplementedError()


class ConditionFieldSpecificLimit(Condition):

    def check(self, events, field=None, **kwargs):

        login_errors = list(utils.filter_events_by_type(events, "LOGIN_ERROR"))
        self.logger.info(f"{field} - Login errors: {len(login_errors)}")
        timestamp_to_events = utils.build_timestamp_to_event_dict(login_errors)
        # Very likely a source for bugs, since the now is evaluated every iteration
        times = [x for x in timestamp_to_events.keys() if x - datetime.datetime.now() < self.timeframe]

        # Check fails/IP
        count_map = {}
        field_content_to_any_event = {}
        for t in times:
            # try main structure
            field_content = timestamp_to_events.get(t, {}).get(field, None)
            # try details
            if not field_content:
                field_content = timestamp_to_events.get(t, {}).get("details", {}).get(field, None)
            # continue if still not found
            if not field_content:
                self.logger.debug(f"Could not find event {field} content")
                continue
            if field_content in count_map:
                count_map[field_content] += 1
            else:
                count_map[field_content] = 1
                field_content_to_any_event.update({field_content: timestamp_to_events[t]})

        self.logger.debug(f"Count Map: {count_map}")
        above_values = [x for x in count_map if count_map[x] > self.threshold]
        results = []
        for v in above_values:
            results.append((field_content_to_any_event[v], count_map[v], field))
        return results