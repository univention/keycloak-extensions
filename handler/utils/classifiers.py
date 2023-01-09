"""
Utilities to aggregate events on different paramenters.
"""


def aggregate_on_code_id(events):
    aggregated_result = {}
    for e in events:
        if e["details"]["code_id"] in aggregated_result:
            aggregated_result[e["details"]["code_id"]].append(e)
        else:
            aggregated_result[e["details"]["code_id"]] = [e]
    return aggregated_result


def aggregate_on_ip(events):
    aggregated_result = {}
    for e in events:
        if e["ipAddress"] in aggregated_result:
            aggregated_result[e["ipAddress"]].append(e)
        else:
            aggregated_result[e["ipAddress"]] = [e]
    return aggregated_result
