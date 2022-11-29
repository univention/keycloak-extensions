import os
import ssl
import smtplib
import logging


class Email:

    def __init__(self):
        self.port = os.environ.get("SMTP_SERVER_PORT")
        self.sender_mail = os.environ.get("SENDER_MAIL")
        self.sender_server = os.environ.get("SMTP_SERVER")
        self.sender_password = os.environ.get("SMTP_PASSWORD")

        # Configure logging
        log_level = os.environ.get('LOG_LEVEL', 'INFO')
        logging.basicConfig(
            format='%(asctime)s %(levelname)s %(message)s',
            datefmt='%d/%m/%Y %I:%M:%S',
            level=log_level)
        self.logger = logging.getLogger(__name__)

    def send(target: str, **kwargs):
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
