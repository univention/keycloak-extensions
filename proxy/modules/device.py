import datetime
import os
from uuid import uuid4
import logging

from sqlalchemy import or_


from modules import email
from app import db
from app import File


IDENTIFIER_COOKIE_NAME = "UNIVENTION_DEVICE"
DEVICE_FINGERPRINT_COOKIE = "DEVICE_FINGERPRINT"

mail = email.Email()


class Device:

    def __init__(self, ip, user_agent):

        # Configure logging
        log_level = os.environ.get('LOG_LEVEL', 'INFO')
        logging.basicConfig(
            format='%(asctime)s %(levelname)s %(message)s',
            datefmt='%d/%m/%Y %I:%M:%S',
            level=log_level)
        self.logger = logging.getLogger(__name__)

        self.uuid = None
        self.uuid_fingerprint = None
        self.ip = ip
        self.user_agent = user_agent

    def get_device_by_ip_or_user_agent(self):
        result = db.session.query(File).filter(
            or_(File.agent == self.user_agent, File.ip == self.ip)).first()
        if not result:
            self.logger.debug(
                f"Unknown User Agent {self.user_agent} on {self.ip}")
        return result

    def get_device_by_cookie(self, cookies):
        result = None
        if IDENTIFIER_COOKIE_NAME in cookies:
            self.uuid = cookies.get(IDENTIFIER_COOKIE_NAME)
            self.logger.debug("Cookie ID:", self.uuid)
        if self.uuid:
            result = db.session.query(File).filter(
                File.uuid == self.uuid).first()
            if not result:
                self.logger.debug("Bad Device ID, will overwrite")
        return self.uuid, result

    def get_device_by_fingerprint_cookie(self, cookies, response):
        if DEVICE_FINGERPRINT_COOKIE in cookies:
            self.uuid_fingerprint = cookies.get(
                DEVICE_FINGERPRINT_COOKIE)
            self.logger.debug("Device Fingerprint:", self.uuid_fingerprint)
        if self.uuid_fingerprint:
            result_fp = db.session.query(File).filter(
                File.uuid == self.uuid_fingerprint).first()
            self.logger.debug("Result Fingerprint",
                              self.uuid_fingerprint, result_fp)
        if result_fp:
            self.logger.info("Known Device: " + "\n".join(str(x)
                                                          for x in [ua, ip, uuid_string, uuid_string_fp]))
        else:
            self.logger.info("New device mail, saving details")
            self.uuid = str(uuid4())
            expiry = datetime.datetime.now() + datetime.timedelta(days=10000)
            response.set_cookie(IDENTIFIER_COOKIE_NAME.encode(), self.uuid.encode(),
                                expires=expiry)
            db.session.merge(File(uuid=self.uuid, agent=self.user_agent,
                                  ip=self.ip))
            db.session.commit()

            mail.send(user_agent=ua, ip=ip, cookie_id=self.uuid,
                      fingerprint=self.uuid_fingerprint)

        if self.uuid_fingerprint and not result_fp:
            self.logger.debug("Bad Device ID FP, Overwriting")
            db.session.merge(File(uuid=self.uuid_fingerprint,
                             agent=self.user_agent, ip=self.ip))
            db.session.commit()

        return response
