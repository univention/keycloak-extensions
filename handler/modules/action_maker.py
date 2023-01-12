import os
import logging
from datetime import datetime, timedelta

from database import session
from models.action import Action
from utils import classifiers


class ActionMaker:
    """
    Evaluate events, take decisions and call the shots.
    """

    def __init__(self):
        self.attempts_for_ip_block = int(
            os.environ.get("FAILED_ATTEMPTS_FOR_IP_BLOCK", 7))
        self.attempts_for_device_block = int(
            os.environ.get("FAILED_ATTEMPTS_FOR_DEVICE_BLOCK", 5))
        self.attempts_for_captcha_trigger = int(
            os.environ.get("FAILED_ATTEMPTS_FOR_CAPTCHA_TRIGGER", 3))

        self.ip_protection_enabled = os.environ.get(
            "IP_PROTECTION_ENABLE", "True").lower() == "true"
        self.device_protection_enabled = os.environ.get(
            "DEVICE_PROTECTION_ENABLE", "True").lower() == "true"
        self.captcha_protection_enabled = os.environ.get(
            "CAPTCHA_PROTECTION_ENABLE", "True").lower() == "true"

        self.expire_in = int(os.environ.get("AUTO_EXPIRE_RULE_IN_MINS", 5))

        # Configure logging
        log_level = os.environ.get('LOG_LEVEL', 'INFO')
        logging.basicConfig(
            format='%(asctime)s %(levelname)s %(message)s',
            datefmt='%d/%m/%Y %I:%M:%S',
            level=log_level)
        self.logger = logging.getLogger(__name__)

    def take_actions(self, events):
        events_aggregated_by_ip = classifiers.aggregate_on_ip(events)
        events_aggregated_by_code_id = classifiers.aggregate_on_code_id(events)
        self.take_ip_actions(events_aggregated_by_ip)
        self.take_device_actions(events_aggregated_by_code_id)
        return

    def take_ip_actions(self, events_aggregated_by_ip):
        for ip, ip_events in events_aggregated_by_ip.items():
            previous_action_for_ip = session.query(
                Action).filter(Action.ip_address == ip).first()
            # Already an IP block issued for this IP
            if previous_action_for_ip is not None:
                if previous_action_for_ip.action == "ip":
                    self.logger.debug(
                        f"IP block already exists for this IP ({ip})")
                    continue
            # Enough attempts for reCaptcha, not enough for IP block
            if self.attempts_for_captcha_trigger <= len(ip_events) < self.attempts_for_ip_block:
                # Already a reCaptcha action issued for this IP
                if previous_action_for_ip is not None:
                    if previous_action_for_ip.action == "captcha":
                        self.logger.debug(
                            f"reCaptcha action already exists for this IP ({ip})")
                        continue
                if not self.captcha_protection_enabled:
                    continue
                action = Action(
                    "captcha",
                    datetime.now() + timedelta(minutes=self.expire_in),
                    ip_address=ip
                )
                session.add(action)
                self.logger.info(
                    f"Issuing the following based on {len(ip_events)} failed login attempts:")
                self.logger.info(action)
                continue
            # Enough attempts for device block, not enough for IP block
            if len(ip_events) >= self.attempts_for_ip_block:
                # If reCaptcha action already issued, delete it
                if previous_action_for_ip is not None:
                    if previous_action_for_ip.action == "captcha":
                        self.logger.debug(
                            f"reCaptcha action for this IP ({ip}), will be updated now")
                        session.query(Action).filter(
                            Action.id == previous_action_for_ip.id).delete()
                if not self.ip_protection_enabled:
                    continue
                # Issue new ip block
                action = Action(
                    "ip",
                    datetime.now() + timedelta(minutes=self.expire_in),
                    ip_address=ip
                )
                session.add(action)
                self.logger.info(
                    f"Issuing the following based on {len(ip_events)} failed login attempts:")
                self.logger.info(action)
        session.commit()

    def take_device_actions(self, events_aggregated_by_code_id):
        for code_id, code_id_events in events_aggregated_by_code_id.items():
            previous_action_for_device_ip = session.query(Action).filter(
                Action.ip_address == code_id_events[0].get("ipAddress")
            ).filter(Action.action == "ip").first()
            # IP block already issued for the device IP: skip
            if previous_action_for_device_ip:
                self.logger.debug(
                    f"IP action exists for this device ({code_id}), device block not needed")
                continue
            previous_action_for_device = session.query(Action).filter(
                Action.keycloak_device_id == code_id,
            ).first()
            # Already a device block issued for this device
            if previous_action_for_device is not None:
                if previous_action_for_device.action == "device":
                    self.logger.debug(
                        f"Device block already exists for this device ({code_id})")
                    continue
            # Enough attempts for reCaptcha, not enough for device block
            if self.attempts_for_captcha_trigger <= len(code_id_events) < self.attempts_for_device_block:
                # Already a reCaptcha action issued for this device
                if previous_action_for_device is not None:
                    if previous_action_for_device.action == "captcha":
                        self.logger.debug(
                            f"reCaptcha action already exists for this device ({code_id})")
                        continue
                if not self.captcha_protection_enabled:
                    continue
                action = Action(
                    "captcha",
                    datetime.now() + timedelta(minutes=self.expire_in),
                    keycloak_device_id=code_id,
                )
                session.add(action)
                self.logger.info(
                    f"Issuing the following based on {len(code_id_events)} failed login attempts:")
                self.logger.info(action)
                continue
            # Too many attempts for reCaptcha, block device.
            if len(code_id_events) >= self.attempts_for_device_block:
                # If reCaptcha action already issued, delete it
                if previous_action_for_device is not None:
                    if previous_action_for_device.action == "captcha":
                        self.logger.debug(
                            f"reCaptcha action for this device ({code_id}), will be updated now")
                        session.query(Action).filter(
                            Action.id == previous_action_for_device.id).delete()
                if not self.device_protection_enabled:
                    continue
                # Issue new device block
                action = Action(
                    "device",
                    datetime.now() + timedelta(minutes=self.expire_in),
                    keycloak_device_id=code_id,
                )
                session.add(action)
                self.logger.info(
                    f"Issuing the following based on {len(code_id_events)} failed login attempts:")
                self.logger.info(action)
        session.commit()

    def remove_expired_actions(self):
        results = session.query(Action).filter(
            Action.expiration <= datetime.now()).delete()
        session.commit()
        self.logger.debug("Removed expired actions")
        self.logger.debug(results)
        return results
