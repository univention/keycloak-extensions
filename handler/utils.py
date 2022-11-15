import datetime


def parse_event_date(e):
    time_in_json = int(e["time"])  # careful this is unix in ms
    time_parsed = datetime.datetime.fromtimestamp(time_in_json // 1000)
    e["time"] = time_parsed
    return e


def build_timestamp_to_event_dict(events):
    time_event_dict = {}
    for e in events:
        time_event_dict.update({e["time"]: e})
    return time_event_dict


def filter_events_by_type(events, type_string):
    if not type_string:
        return events
    return [e for e in events if e["type"] == type_string]


def filter_out_token_errors(events, field, not_value):
    return filter(lambda e: e.get("details").get(field) != not_value, events)
