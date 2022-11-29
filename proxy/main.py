#!/usr/bin/python3

import json
import ssl
import os
import requests
import flask
import datetime
import sys
import uuid
import smtplib
import logging
from http import HTTPStatus

from sqlalchemy import Column, String, or_
from flask_sqlalchemy import SQLAlchemy

INHERENT_HEADERS = ["content-encoding",
                    "content-length", "transfer-encoding", "connection"]
IDENTIFIER_COOKIE_NAME = "UNIVENTION_DEVICE"
SUSPICIOUS_REQUEST_HEADER = "X-SUSPICIOUS-REQUEST"
KEYCLOAK_SESSION_ID_COOKIE = "AUTH_SESSION_ID"
DEVICE_FINGERPRINT_COOKIE = "DEVICE_FINGERPRINT"
HEADER_TRUE = 1
CONTENT_TYPE_APPLICATION_JSON = {"Content-Type": "application/json"}

APP_NAME = "Smart Flask Reverse Proxy"
app = flask.Flask(APP_NAME)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
db = SQLAlchemy(app)


def handle_api_call(frequest):

    if flask.request.method == "GET":
        r = flask.Response(json.dumps(app.config["ACTIONS"], indent=2), HTTPStatus.OK,
                           headers=CONTENT_TYPE_APPLICATION_JSON)
        return r

    json_dict = frequest.json
    if not json_dict:
        return ("API Requested without application/json", HTTPStatus.BAD_REQUEST)

    condition = json_dict["condition"]        # device_id, ip
    action = json_dict["action"]              # block, set-header
    # the ip or device id to check for
    value = json_dict.get("value")
    # time at which this rule expires
    valid_until = json_dict.get("valid_until")

    action_uuid = action + condition + value + valid_until

    if flask.request.method == "POST":

        if action_uuid in app.config["ACTIONS"]:
            return ("Action already exists", HTTPStatus.CONFLICT)
        app.config["ACTIONS"].update({action_uuid: dict(json_dict)})

        if value not in app.config["INDEX"]:
            app.config["INDEX"].update({value: [action_uuid]})
        else:
            app.config["INDEX"][value].append(action_uuid)

    elif flask.request.method == "DELETE":

        app.config["ACTIONS"].pop(action_uuid)
        actions = app.config["INDEX"][value]

        if len(actions) == 1:
            app.config["INDEX"].pop(value)
        else:
            app.config["INDEX"][value].remove(action_uuid)

    else:
        return ("Method Not Allowed", HTTPStatus.METHOD_NOT_ALLOWED)

    return ("OK", HTTPStatus.OK)


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


@app.route("/fingerprintjs/v3", methods=["GET"])
def fingerprint():
    return flask.send_from_directory("static", "fingerprint.js")


@app.route("/proxy-api", methods=["GET"])
def proxy_api_passthrough():
    returnflask.Response(
        json.dumps(app.config["ACTIONS"], indent=2),
        HTTPStatus.OK,
        headers=CONTENT_TYPE_APPLICATION_JSON
    )


@app.route("/<path:path>", methods=["GET", "POST", "DELETE", "PUT"])
def proxy(path):

    if path == "flask-redirect-api":
        return handle_api_call(flask.request)
    elif path == "fingerprintjs/v3":
        return flask.send_from_directory("static", "fingerprint.js")

    # DO NOT MOVE THIS DOWN - NEEDS TO BE FIRST CALL #
    data = flask.request.get_data()

    # find correct request method #
    request_function = getattr(requests, flask.request.method.lower())

    # make request #
    fullpath = flask.request.full_path
    request_url = app.config["BACKEND"] + fullpath
    incoming_headers = flask.request.headers

    # check ip block actions #
    check_result = check_ip(flask.request)
    if check_result is None:
        return ("Too Many Requests from this IP", HTTPStatus.TOO_MANY_REQUESTS)
    if check_result:
        incoming_headers.update(check_result)

    # check cookie block actions #
    check_result = check_cookie(flask.request, KEYCLOAK_SESSION_ID_COOKIE)
    if check_result is None:
        return ("This Device has made too many requests", HTTPStatus.TOO_MANY_REQUESTS)
    if check_result:
        incoming_headers.update(check_result)

    r = request_function(request_url, headers=incoming_headers,
                         cookies=flask.request.cookies, data=data,
                         auth=flask.request.authorization,
                         allow_redirects=False)

    # filter response headers #
    backend_headers = []
    content_type = ""
    for k, v in r.headers.items():
        if not k.lower() in INHERENT_HEADERS:
            if k == "Content-Type":
                content_type = v
            backend_headers.append((k, v))

    # inject fingerprint #
    html = '''<script>
      // Initialize the agent at application startup.
      const fpPromise = import('/fingerprintjs/v3')
        .then(FingerprintJS => FingerprintJS.load())

      // Get the visitor identifier when you need it.
      fpPromise
        .then(fp => fp.get())
        .then(result => {
          // This is the visitor identifier:
          const visitorId = result.visitorId
          console.log(visitorId)
          document.cookie = 'DEVICE_FINGERPRINT=' + visitorId+ ';path=/';
        })
    </script> '''.encode()

    response = None
    if "text/html" in content_type and "openid-connect/auth" in path:
        print("Injecting JS..:")
        response = flask.Response(
            r.content + html, r.status_code, headers=backend_headers)
    else:
        response = flask.Response(
            r.content, r.status_code, headers=backend_headers)

    for c in r.cookies:
        response.set_cookie(c.name, c.value)

    if "login-actions" in path:

        fail_counter = 0
        ua = flask.request.headers.get('User-Agent')
        ip = flask.request.headers.get("X-Forwarded-For")
        if not ip:
            ip = flask.request.remote_addr

        # ip / ua #
        result = db.session.query(File).filter(
            or_(File.agent == ua, File.ip == ip)).first()
        if not result:
            print("Unknown {} on {}".format(ua, ip))
            fail_counter += 1

        # persistent cookie #
        # check if cookie exists & valid #
        uuid_string = None
        uuid_string_fp = None
        result = None
        result_fp = None

        # print(flask.request.cookies)
        if IDENTIFIER_COOKIE_NAME in flask.request.cookies:
            uuid_string = flask.request.cookies.get(IDENTIFIER_COOKIE_NAME)
            print("Cookie ID:", uuid_string)
        if DEVICE_FINGERPRINT_COOKIE in flask.request.cookies:
            uuid_string_fp = flask.request.cookies.get(
                DEVICE_FINGERPRINT_COOKIE)
            print("Device Fingerprint:", uuid_string_fp)
        if uuid_string:
            result = db.session.query(File).filter(
                File.uuid == uuid_string).first()
            if not result:
                print("Bad Device ID, Overwriting")

        if uuid_string_fp:
            result_fp = db.session.query(File).filter(
                File.uuid == uuid_string_fp).first()

        # if not valid
        # if not result and not result_fp
        print("Result fp", uuid_string_fp, result_fp)
        print("Result nofp", uuid_string, result)
        if not result_fp:
            print("New device mail")
            uuid_string = str(uuid.uuid4())
            expiry = datetime.datetime.now() + datetime.timedelta(days=10000)
            response.set_cookie(IDENTIFIER_COOKIE_NAME.encode(), uuid_string.encode(),
                                expires=expiry)
            db.session.merge(File(uuid=uuid_string, agent=ua,
                                  ip=ip))
            db.session.commit()

            send_mail(user_agent=ua, ip=ip, cookie_id=uuid_string,
                      fingerprint=uuid_string_fp)
        else:
            print("Known Device: " + "\n".join(str(x)
                  for x in [ua, ip, uuid_string, uuid_string_fp]))

        if uuid_string_fp and not result_fp:
            print("Bad Device ID FP, Overwriting")
            db.session.merge(File(uuid=uuid_string_fp, agent=ua, ip=ip))
            db.session.commit()

    return response


def send_mail(**kwargs):

    if os.path.isfile("last_mail"):
        with open("last_mail") as f:
            now = datetime.datetime.now()
            content = f.read()
            if content:
                dif = now - \
                    datetime.datetime.fromtimestamp(int(float(content)))
                if dif < datetime.timedelta(seconds=os.environ["MAIL_BACKOFF_TIME"]):
                    print("Not sending Mail - still in backoff time!")
                    return True

    with open("last_mail", "w") as f:
        f.write(str(int(datetime.datetime.now().timestamp())))

    print("Sending Mail...")

    port = os.environ["SMTP_SERVER_PORT"]  # For SSL

    # Create a secure SSL context
    context = ssl.create_default_context()
    targets = os.environ["TARGET_EMAILS"]
    sender_mail = os.environ["SENDER_MAIL"]
    sender_server = os.environ["SMTP_SERVER"]
    sender_password = os.environ["SMTP_PASSWORD"]

    for target_mail in targets:

        with smtplib.SMTP_SSL(sender_server, port, context=context) as server:
            server.login(sender_mail, sender_password)

            output = []
            for k, v in kwargs.items():
                output.append("{}: {}".format(k, v))
            message = "Subject: New Device Login\n\n\nLogin from New Device:\n\n"
            message += "\n\n".join(output)
            server.sendmail(sender_mail, target_mail, message)


@app.before_first_request
def init():
    app.config["DB"] = db
    app.config["API_SECRET"] = os.environ["API_SECRET"]
    app.config["ACTIONS"] = {}
    app.config["INDEX"] = {}
    app.config["BACKEND"] = "{}://{}".format(os.environ["KEYCLOAK_PROTOCOL"],
                                             os.environ["KEYCLOAK_SERVER"])
    db.create_all()


class File(db.Model):
    __tablename__ = "devices"
    uuid = Column(String, primary_key=True)
    agent = Column(String)
    ip = Column(String)


# keep this for debugging
if __name__ == "__main__":

    log = logging.getLogger('werkzeug')
    log.setLevel(logging.WARNING)

    app.run(host=os.environ["INTERFACE"], port=os.environ["PORT"])
