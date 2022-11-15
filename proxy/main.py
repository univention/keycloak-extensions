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
import http.HTTPStatus as status

from sqlalchemy import Column, String, or_
from flask_sqlalchemy import SQLAlchemy

INHERENT_HEADERS = ["content-encoding", "content-length", "transfer-encoding", "connection"]
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


def handleApiCall(frequest):

    if flask.request.method == "GET":
        r = flask.Response(json.dumps(app.config["ACTIONS"], indent=2), status.OK,
                           headers=CONTENT_TYPE_APPLICATION_JSON)
        return r

    jsonDict = frequest.json
    if not jsonDict:
        return ("API Requested without application/json", status.BAD_REQUEST)

    condition = jsonDict["condition"]        # device_id, ip
    action = jsonDict["action"]              # block, set-header
    value = jsonDict.get("value")            # the ip or device id to check for
    validUntil = jsonDict.get("validUntil")  # time at which this rule expires

    actionUuid = action + condition + value + validUntil

    if flask.request.method == "POST":

        if actionUuid in app.config["ACTIONS"]:
            return ("Action already exists", status.CONFLICT)
        app.config["ACTIONS"].update({actionUuid: dict(jsonDict)})

        if value not in app.config["INDEX"]:
            app.config["INDEX"].update({value: [actionUuid]})
        else:
            app.config["INDEX"][value].append(actionUuid)

    elif flask.request.method == "DELETE":

        app.config["ACTIONS"].pop(actionUuid)
        actions = app.config["INDEX"][value]

        if len(actions) == 1:
            app.config["INDEX"].pop(value)
        else:
            app.config["INDEX"][value].remove(actionUuid)

    else:
        return ("Method Not Allowed", status.METHOD_NOT_ALLOWED)

    return ("OK", status.OK)


def checkIp(frequest):

    ip = frequest.headers.get("X-Forwarded-For")
    if not ip:
        ip = frequest.remote_addr

    actionUuidIpList = app.config["INDEX"].get(ip)
    if actionUuidIpList:
        for actionUuidIp in actionUuidIpList:
            if actionUuidIp:
                action = app.config["ACTIONS"].get(actionUuidIp)
                if action["condition"] != "ip":
                    continue
                if action["action"] == "set-header":
                    return {SUSPICIOUS_REQUEST_HEADER: HEADER_TRUE}
                if action["action"] == "block":
                    return None

    return []


def checkCookie(frequest, cookieName):

    # just in case flask ever changes cookie behaviour
    cookieContent = frequest.cookies.get(cookieName)
    if not cookieContent and len(frequest.cookies) > 0:
        return []
    elif not cookieContent:
        cookieContent = frequest.cookies[0].get(cookieName)

    # sanity check
    if not cookieContent:
        return []

    actionUuidValueList = app.config["INDEX"].get(cookieContent)
    if actionUuidValueList:
        for actionUuidValue in actionUuidValueList:
            if actionUuidValue:
                action = app.config["ACTIONS"].get(actionUuidValue)
                if action["condition"] != "cookie_contains":
                    continue
                if action["action"] == "set-header":
                    print("Setting Header because of Cookie", file=sys.stderrr)
                    return {SUSPICIOUS_REQUEST_HEADER: HEADER_TRUE}
                if action["action"] == "block":
                    print("Blocking Cookie...", file=sys.stderr)
                    return None

    return []


@app.route("/<path:path>", methods=["GET", "POST", "DELETE", "PUT"])
def proxy(path):

    if path == "flask-redirect-api":
        return handleApiCall(flask.request)
    elif path == "fingerprintjs/v3":
        return flask.send_from_directory("static", "fingerprint.js")

    # DO NOT MOVE THIS DOWN - NEEDS TO BE FIRST CALL #
    data = flask.request.get_data()

    # find correct request method #
    requestFunction = getattr(requests, flask.request.method.lower())

    # make request #
    fullpath = flask.request.full_path
    requestUrl = app.config["BACKEND"] + fullpath
    incomingHeaders = flask.request.headers

    # check ip block actions #
    checkResult = checkIp(flask.request)
    if checkResult is None:
        return ("Too Many Requests from this IP", status.TOO_MANY_REQUESTS)
    if checkResult:
        incomingHeaders.update(checkResult)

    # check cookie block actions #
    checkResult = checkCookie(flask.request, KEYCLOAK_SESSION_ID_COOKIE)
    if checkResult is None:
        return ("This Device has made too many requests", status.TOO_MANY_REQUESTS)
    if checkResult:
        incomingHeaders.update(checkResult)

    r = requestFunction(requestUrl, headers=incomingHeaders,
                        cookies=flask.request.cookies, data=data,
                        auth=flask.request.authorization,
                        allow_redirects=False)

    # filter response headers #
    backendHeaders = []
    contentType = ""
    for k, v in r.headers.items():
        if not k.lower() in INHERENT_HEADERS:
            if k == "Content-Type":
                contentType = v
            backendHeaders.append((k, v))

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
    if "text/html" in contentType and "openid-connect/auth" in path:
        print("Injecting JS..:")
        response = flask.Response(r.content + html, r.status_code, headers=backendHeaders)
    else:
        response = flask.Response(r.content, r.status_code, headers=backendHeaders)

    for c in r.cookies:
        response.set_cookie(c.name, c.value)

    if "login-actions" in path:

        failCounter = 0
        ua = flask.request.headers.get('User-Agent')
        ip = flask.request.headers.get("X-Forwarded-For")
        if not ip:
            ip = flask.request.remote_addr

        # ip / ua #
        result = db.session.query(File).filter(or_(File.agent == ua, File.ip == ip)).first()
        if not result:
            print("Unknown {} on {}".format(ua, ip))
            failCounter += 1

        # persistent cookie #
        # check if cookie exists & valid #
        uuidString = None
        uuidStringFp = None
        result = None
        resultFp = None

        #print(flask.request.cookies)
        if IDENTIFIER_COOKIE_NAME in flask.request.cookies:
            uuidString = flask.request.cookies.get(IDENTIFIER_COOKIE_NAME)
            print("Cookie ID:", uuidString)
        if DEVICE_FINGERPRINT_COOKIE in flask.request.cookies:
            uuidStringFp = flask.request.cookies.get(DEVICE_FINGERPRINT_COOKIE)
            print("Device Fingerprint:", uuidStringFp)
        if uuidString:
            result = db.session.query(File).filter(File.uuid == uuidString).first()
            if not result:
                print("Bad Device ID, Overwriting")

        if uuidStringFp:
            resultFp = db.session.query(File).filter(File.uuid == uuidStringFp).first()

        # if not valid
        # if not result and not resultFp
        print("Result fp", uuidStringFp, resultFp)
        print("Result nofp", uuidString, result)
        if not resultFp:
            print("New device mail")
            uuidString = str(uuid.uuid4())
            expiry = datetime.datetime.now() + datetime.timedelta(days=10000)
            response.set_cookie(IDENTIFIER_COOKIE_NAME.encode(), uuidString.encode(),
                                expires=expiry)
            db.session.merge(File(uuid=uuidString, agent=ua,
                                  ip=ip))
            db.session.commit()

            sendMail(user_agent=ua, ip=ip, cookieId=uuidString, fingerprint=uuidStringFp)
        else:
            print("Known Device: " + "\n".join(str(x) for x in [ua, ip, uuidString, uuidStringFp]))

        if uuidStringFp and not resultFp:
            print("Bad Device ID FP, Overwriting")
            db.session.merge(File(uuid=uuidStringFp, agent=ua, ip=ip))
            db.session.commit()

    return response


def sendMail(**kwargs):

    if os.path.isfile("last_mail"):
        with open("last_mail") as f:
            now = datetime.datetime.now()
            content = f.read()
            if content:
                dif = now - datetime.datetime.fromtimestamp(int(float(content)))
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
    senderMail = os.environ["SENDER_MAIL"]
    senderServer = os.environ["SMTP_SERVER"]
    senderPassword = os.environ["SMTP_PASSWORD"]

    for targetMail in targets:

        with smtplib.SMTP_SSL(senderServer, port, context=context) as server:
            server.login(senderMail, senderPassword)

            output = []
            for k, v in kwargs.items():
                output.append("{}: {}".format(k, v))
            message = "Subject: New Device Login\n\n\nLogin from New Device:\n\n"
            message += "\n\n".join(output)
            server.sendmail(senderMail, targetMail, message)


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
