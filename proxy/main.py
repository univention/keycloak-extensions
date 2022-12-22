#!/usr/bin/python3

import json
import ssl
import os
import requests
import logging
import flask
import datetime
import sys
import uuid
import smtplib
import logging
from http import HTTPStatus

from app import app
from utils import check_ip
from utils import check_cookie
from utils import get_action_uuid
from utils import generate_backend_headers
from modules import fingerprint
from modules import email
from modules import device


# FIXME: Move this somewhere else, a config file or so
SUSPICIOUS_REQUEST_HEADER = "X-SUSPICIOUS-REQUEST"
KEYCLOAK_SESSION_ID_COOKIE = "AUTH_SESSION_ID"
HEADER_TRUE = 1
CONTENT_TYPE_APPLICATION_JSON = {"Content-Type": "application/json"}

mail = email.Email()
fprint = fingerprint.Fingerprint()


@app.route("/fingerprintjs/v3", methods=["GET"])
def fingerprint():
    return flask.send_from_directory("static", "fingerprint.js")


@app.route("/proxy-api", methods=["GET"])
def proxy_api_get():
    """
    Handles GET requests to our internal API.

    Returns actions that are currently active.
    """
    return flask.Response(
        json.dumps(app.config["ACTIONS"], indent=2),
        HTTPStatus.OK,
        headers=CONTENT_TYPE_APPLICATION_JSON
    )


@app.route("/proxy-api", methods=["POST"])
def proxy_api_post():
    json_dict = flask.request.json
    if not json_dict:
        return ("API Requested without application/json", HTTPStatus.BAD_REQUEST)
    print(json_dict)
    action_uuid = get_action_uuid(json_dict)
    if action_uuid in app.config["ACTIONS"]:
        return ("Action already exists", HTTPStatus.CONFLICT)
    app.config["ACTIONS"].update({action_uuid: dict(json_dict)})

    value = json_dict.get("value")
    if value not in app.config["INDEX"]:
        app.config["INDEX"].update({value: [action_uuid]})
    else:
        app.config["INDEX"][value].append(action_uuid)
    return ("OK", HTTPStatus.OK)


@app.route("/proxy-api", methods=["DEL"])
def proxy_api_del():
    json_dict = flask.request.json
    if not json_dict:
        return ("API Requested without application/json", HTTPStatus.BAD_REQUEST)
    action_uuid = get_action_uuid(json_dict)
    app.config["ACTIONS"].pop(action_uuid)
    actions = app.config["INDEX"][value]

    if len(actions) == 1:
        app.config["INDEX"].pop(value)
    else:
        app.config["INDEX"][value].remove(action_uuid)
    return ("OK", HTTPStatus.OK)


@app.route("/<path:path>", methods=["GET", "POST", "DELETE", "PUT"])
def proxy(path):
    """
    Handles requests to Keycloak's API
    """

    # DO NOT MOVE THIS DOWN - NEEDS TO BE FIRST CALL
    data = flask.request.get_data()

    # Find correct request method
    request_function = getattr(requests, flask.request.method.lower())

    # Make request
    fullpath = flask.request.full_path
    request_url = app.config["BACKEND"] + fullpath
    incoming_headers = flask.request.headers

    # Check ip block actions
    check_result = check_ip(flask.request)
    if check_result is None:
        return ("Too Many Requests from this IP", HTTPStatus.TOO_MANY_REQUESTS)
    if check_result:
        incoming_headers.update(check_result)

    # Check cookie block actions
    check_result = check_cookie(flask.request, KEYCLOAK_SESSION_ID_COOKIE)
    if check_result is None:
        return ("This Device has made too many requests", HTTPStatus.TOO_MANY_REQUESTS)
    if check_result:
        incoming_headers.update(check_result)

    r = request_function(request_url, headers=incoming_headers,
                         cookies=flask.request.cookies, data=data,
                         auth=flask.request.authorization,
                         allow_redirects=False)

    # Filter response headers
    content_type, backend_headers = generate_backend_headers(r.headers)

    # Inject fingerprintjs/v3 if needed
    response = None
    if "text/html" in content_type and "openid-connect/auth" in path:
        response = fprint.inject_fingerprint(r, backend_headers)
    else:
        response = flask.Response(
            r.content, r.status_code, headers=backend_headers)

    # Put the cookies in the new response
    for c in r.cookies:
        response.set_cookie(c.name, c.value)

    if "login-actions" in path:

        ua = flask.request.headers.get('User-Agent')
        ip = flask.request.headers.get("X-Forwarded-For")
        if not ip:
            ip = flask.request.remote_addr

        dev = device.Device(ip, ua)
        dev.get_device_by_ip_or_user_agent()
        dev.get_device_by_cookie(flask.request.cookies)
        response = dev.get_device_by_fingerprint_cookie(
            flask.request.cookies, response)

    return response


app.run(host="0.0.0.0", port=os.environ["PORT"])
