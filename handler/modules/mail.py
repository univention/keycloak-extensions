import os
import logging
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


class Email:
    def __init__(self, receiver, details):
        self.receiver = receiver
        self.message = MIMEMultipart()
        self.message['To'] = receiver
        self.message['Subject'] = os.environ.get(
            "NEW_DEVICE_LOGIN_SUBJECT", "New device login")
        self.message['From'] = os.environ.get("SENDER_EMAIL", None)
        self.generate_body(details)
        self.sender = os.environ.get("SENDER_EMAIL", None)
        self.password = os.environ.get("SENDER_EMAIL_PASSWORD", None)
        assert self.sender is not None
        assert self.password is not None
        self.smtp_server = os.environ.get("SMTP_SERVER", None)
        self.smtp_port = int(os.environ.get("SMTP_PORT", 587))

        # Configure logging
        log_level = os.environ.get('LOG_LEVEL', 'INFO')
        logging.basicConfig(
            format='%(asctime)s %(levelname)s %(message)s',
            datefmt='%d/%m/%Y %I:%M:%S',
            level=log_level)
        self.logger = logging.getLogger(__name__)

    def generate_body(self, details: dict):
        details_str = ""
        for key, value in details.items():
            details_str += f"   {key}: {value}\n"
        body = f"""Hello,
    
You just logged in from a new device. The device details are:

{details_str}

If you don't recognize the device, please take actions or contact your administrator.

Best regards,
Keycloak.
    """

        self.message.attach(MIMEText(body))

    def send(self):
        self.logger.debug(f"Sending email to {self.receiver}")
        self.logger.debug("")
        context = ssl.create_default_context()

        # with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(self.sender, self.password)
            server.sendmail(self.sender, self.receiver,
                            self.message.as_string())