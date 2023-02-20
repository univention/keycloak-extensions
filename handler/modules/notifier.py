import os
import logging

from database import session
from models.device import Device
from modules import mail


class Notifier:

    def __init__(self, keycloak):
        self.keycloak = keycloak

        # Configure logging
        log_level = os.environ.get('LOG_LEVEL', 'INFO')
        logging.basicConfig(
            format='%(asctime)s %(levelname)s %(message)s',
            datefmt='%d/%m/%Y %I:%M:%S',
            level=log_level)
        self.logger = logging.getLogger(__name__)

    def notify_user(self, user_id: str, details: dict):
        user_email = self.keycloak.get_user_email(user_id)
        if user_email is None:
            return
        e = mail.Email(user_email, details)
        e.send()

    def notify_new_logins(self):
        new_logins = session.query(Device).filter(Device.is_notified == False)
        for new_login in new_logins:
            self.notify_user(
                new_login.user_id,
                {
                    "Time": new_login.created_at,
                    "Device ID": new_login.keycloak_device_id,
                    "Fingerprint": new_login.fingerprint_device_id
                })
            new_login.is_notified = True
        session.commit()
