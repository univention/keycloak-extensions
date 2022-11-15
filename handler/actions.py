import smtplib
import json
import ssl
import requests
import os
import datetime

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ActionDelegate:

    def __init__(self, state, args, fails, condition):
        self.state = state
        self.args = args
        self.proxy = "http://{}/flask-redirect-api".format(args.kc_proxy)
        self.ucs_udm_rest = args.udm_rest_base_url
        self.udm_rest_user = args.udm_rest_user
        self.udm_rest_password = args.udm_rest_password
        self.udm_rest_base_url = "https://{user}:{password}@{uri}".format(
            user=self.udm_rest_user, password=self.udm_rest_password, uri=self.ucs_udm_rest)
        self.fails = fails
        self.condition = condition

        if(self.condition == "ip_address"):
            self.condition_value = "ip"
            self.proxy_condition = state.get("ip_address")
        elif(self.condition == "code_id"):
            self.condition_value = "cookie_contains"
            self.proxy_condition = state.get("details").get("code_id")

    def trigger(self):
        raise NotImplementedError()

    def cleanup(self):
        raise NotImplementedError()


class ActionBlockIpProxy(ActionDelegate):

    def trigger(self):
        if self.fails > 5 and self.condition == "code_id":
            payload = {"action": "block", "condition": self.condition_value,
                       "value": self.proxy_condition}
            r = requests.post(self.proxy, headers={"Content-Type": "application/json"},
                              json=payload)
        if(self.fails > 10):
            payload = {"action": "block", "condition": self.condition_value,
                       "value": self.proxy_condition}
            r = requests.post(self.proxy, headers={"Content-Type": "application/json"},
                              data=json.dumps(payload))

        payload = {"action": "add-header", "condition": self.condition_value,
                   "value": self.proxy_condition}
        r = requests.post(self.proxy, headers={"Content-Type": "application/json"},
                          data=json.dumps(payload))


    def cleanup(self):
        payload = {"action": "block", "condition": self.condition_value,
                   "value": self.proxy_condition}
        r = requests.delete(self.proxy, headers={"Content-Type": "application/json"},
                            data=json.dumps(payload))
        payload = {"action": "add-header", "condition": self.condition_value,
                   "value": self.proxy_condition}
        r = requests.delete(self.proxy, headers={"Content-Type": "application/json"},
                            data=json.dumps(payload))



class ActionSendMail(ActionDelegate):

    def trigger(self):

        if os.path.isfile("last_mail"):
            with open("last_mail") as f:
                now = datetime.datetime.now()
                content = f.read()
                if content:
                    dif = now - datetime.datetime.fromtimestamp(int(float(content)))
                    if dif < datetime.timedelta(minutes=1):
                        return True

        with open("last_mail", "w") as f:
            f.write(str(int(datetime.datetime.now().timestamp())))


        port = 465  # For SSL

        # Create a secure SSL context
        context = ssl.create_default_context()
        return
        with smtplib.SMTP_SSL(self.args.mail_server, port, context=context) as server:
            sender = self.args.mail_user + "@" + self.args.mail_server
            server.login(sender, self.args.mail_pass)

            message = f"Subject: Brute Force Detected\n\n{self.state}\n\nCondition: {self.condition}"

            server.sendmail(sender, self.args.admin_mail, message)

        return True

    def cleanup(self):
        return True
