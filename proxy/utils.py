from datetime import datetime, timedelta
import os
import logging
import flask
from app import app
import sys


INHERENT_HEADERS = ["content-encoding",
                    "content-length", "transfer-encoding", "connection"]
SUSPICIOUS_REQUEST_HEADER = "X-SUSPICIOUS-REQUEST"
HEADER_TRUE = 1


log_level = os.environ.get('LOG_LEVEL', 'DEBUG')
logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%d/%m/%Y %I:%M:%S',
    level=log_level)
logger = logging.getLogger(__name__)


def check_ip(frequest):

    ip = frequest.headers.get("X-Forwarded-For")
    if not ip:
        ip = frequest.remote_addr

    action_uuid_ip_list = app.config["INDEX"].get(ip)
    if action_uuid_ip_list:
        for action_uuid_ip in action_uuid_ip_list:
            if action_uuid_ip:
                action = app.config["ACTIONS"].get(action_uuid_ip)
                if action["condition"] != "ip":
                    continue
                if action["action"] == "set-header":
                    return {SUSPICIOUS_REQUEST_HEADER: HEADER_TRUE}
                if action["action"] == "block":
                    return None

    return []


def check_cookie(frequest, cookie_name):

    # just in case flask ever changes cookie behaviour
    cookie_content = frequest.cookies.get(cookie_name)
    if not cookie_content and len(frequest.cookies) > 0:
        return []
    elif not cookie_content:
        cookie_content = frequest.cookies[0].get(cookie_name)

    # sanity check
    if not cookie_content:
        return []

    action_uuid_value_list = app.config["INDEX"].get(cookie_content)
    if action_uuid_value_list:
        for action_uuid_value in action_uuid_value_list:
            if action_uuid_value:
                action = app.config["ACTIONS"].get(action_uuid_value)
                if action["condition"] != "cookie_contains":
                    continue
                if action["action"] == "set-header":
                    print("Setting Header because of Cookie", file=sys.stderrr)
                    return {SUSPICIOUS_REQUEST_HEADER: HEADER_TRUE}
                if action["action"] == "block":
                    print("Blocking Cookie...", file=sys.stderr)
                    return None

    return []


def get_action_uuid(json_dict):
    condition = json_dict["condition"]        # device_id, ip
    action = json_dict["action"]              # block, set-header
    # the ip or device id to check for
    value = json_dict.get("value")
    # time at which this rule expires
    valid_until = json_dict.get(
        "valid_until", datetime.timestamp(datetime.now() + timedelta(minutes=5)))

    action_uuid = action + condition + value  # + valid_until
    return action_uuid


def generate_backend_headers(original_request_headers):
    """
    Filters response headers.
    """
    backend_headers = []
    content_type = ""
    for k, v in original_request_headers.items():
        if not k.lower() in INHERENT_HEADERS:
            if k == "Content-Type":
                content_type = v
            backend_headers.append((k, v))
    return content_type, backend_headers
