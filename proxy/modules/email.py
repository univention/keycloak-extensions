import os
import ssl
import smtplib
import logging

import datetime


class Email:

    def __init__(self):
        self.port = os.environ.get("SMTP_SERVER_PORT")
        self.sender_mail = os.environ.get("SENDER_MAIL")
        self.sender_server = os.environ.get("SMTP_SERVER")
        self.sender_password = os.environ.get("SMTP_PASSWORD")

        self.backoff_time = os.environ.get("MAIL_BACKOFF_TIME")

        # Configure logging
        log_level = os.environ.get('LOG_LEVEL', 'INFO')
        logging.basicConfig(
            format='%(asctime)s %(levelname)s %(message)s',
            datefmt='%d/%m/%Y %I:%M:%S',
            level=log_level)
        self.logger = logging.getLogger(__name__)

    # FIXME: this is a file approach... maybe a queue should be implemented
    def prevent_flooding(self):
        if not os.path.isfile("last_mail"):
            with open("last_mail", "w") as f:
                f.write(str(int(datetime.datetime.now().timestamp())))
            return False

        with open("last_mail") as f:
            now = datetime.datetime.now()
            content = f.read()
            if not content:
                return False
            dif = now - datetime.datetime.fromtimestamp(int(float(content)))
            if dif < datetime.timedelta(seconds=self.backoff_time):
                self.logger.debug(
                    "Flooding prevention. Not sending Mail: still in backoff time!")
                return True
        return True

    def send(self, target: str, **kwargs):
        if self.prevent_flooding():
            return
        self.logger.debug(f"Sending email to {target}")
        context = ssl.create_default_context()
        # FIXME: if port for startls, this will not work
        with smtplib.SMTP_SSL(sender_server, port, context=context) as server:
            server.login(sender_mail, sender_password)
            # FIXME: add \n at the end of each kwarg
            output = [f"{k}: {v}" for k, v in kwargs.items()]
            message = "Subject: New Device Login\n\n\nLogin from New Device:\n\n"
            message += "\n\n".join(output)
            server.sendmail(sender_mail, target_mail, message)
        self.logger.debug(f"Mail sent to {target}")
