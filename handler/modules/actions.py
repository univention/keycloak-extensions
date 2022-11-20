import smtplib
import ssl
import requests
import os
import datetime

import urllib3

# Why is this here?
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ActionDelegate:

    def __init__(self, state, args, fails, condition):
        # Configure logging
        log_level = os.environ.get('LOG_LEVEL', 'INFO')
        logging.basicConfig(
            format='%(asctime)s %(levelname)s %(message)s',
            datefmt='%d/%m/%Y %I:%M:%S',
            level=log_level)
        self.logger = logging.getLogger(__name__)

        self.ucs_udm_rest = os.environ.get("UDM_REST_BASE_URL")
        self.udm_rest_user =  os.environ.get("UDM_REST_USER")
        self.udm_rest_password =  os.environ.get("UDM_REST_PASSWORD")

        self.state = state
        self.args = args
        self.proxy = "http://{}/flask-redirect-api".format(args.kc_proxy)
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
        self.logger.debug("IP Proxy")
        self.logger.debug(self.proxy)
        if(self.fails > 5 and self.condition == "code_id"):
            payload = {"action": "block", "condition": self.conditionValue,
                       "value": self.proxyCondition}
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
        self.logger.debug(r)

    def cleanup(self):
        self.logger.debug("IP Proxy cleanup")
        payload = {"action": "block", "condition": self.conditionValue,
                   "value": self.proxyCondition}
        r = requests.delete(self.proxy, headers={"Content-Type": "application/json"},
                            data=json.dumps(payload))
        payload = {"action": "add-header", "condition": self.condition_value,
                   "value": self.proxy_condition}
        r = requests.delete(self.proxy, headers={"Content-Type": "application/json"},
                            data=json.dumps(payload))
        self.logger.debug(r)


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

        self.logger.info("Sending Mail...")

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
