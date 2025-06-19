# Like what you see? Join us!
# https://www.univention.com/about-us/careers/vacancies/
#
# Copyright 2020-2024 Univention GmbH
#
# https://www.univention.de/
#
# All rights reserved.
#
# The source code of this program is made available
# under the terms of the GNU Affero General Public License version 3
# (GNU AGPL V3) as published by the Free Software Foundation.
#
# Binary versions of this program provided by Univention to you as
# well as other copyrighted, protected or trademarked materials like
# Logos, graphics, fonts, specific documentations and configurations,
# cryptographic keys etc. are subject to a license agreement between
# you and Univention and not subject to the GNU AGPL V3.
#
# In the case you use this program under the terms of the GNU AGPL V3,
# the program is provided in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License with the Debian GNU/Linux or Univention distribution in file
# /usr/share/common-licenses/AGPL-3; if not, see
# <https://www.gnu.org/licenses/>.
#

import logging
import os

import pytz
from database import session
from keycloak.exceptions import KeycloakGetError
from models.device import Device
from modules import mail


class Notifier:

    def __init__(self, keycloak):
        self.keycloak = keycloak

        # Configure logging
        log_level = os.environ.get("LOG_LEVEL", "INFO")
        logging.basicConfig(
            format="%(asctime)s %(levelname)s %(message)s",
            datefmt="%d/%m/%Y %I:%M:%S",
            level=log_level,
        )
        self.logger = logging.getLogger(__name__)
        self.enabled = (
            os.environ.get(
                "NEW_DEVICE_LOGIN_NOTIFICATION_ENABLE", "true").lower()
            == "true"
        )

        # Get timezone from environment variable
        email_timezone = os.environ.get("EMAIL_TIMEZONE", "UTC")
        try:
            self.timezone = pytz.timezone(email_timezone)
            self.timezone_name = email_timezone
        except pytz.exceptions.UnknownTimeZoneError:
            self.logger.warning(
                f"Unknown timezone '{email_timezone}'. Falling back to UTC."
            )
            self.timezone = pytz.timezone("UTC")
            self.timezone_name = "UTC"

    def notify_user(self, user_id: str, details: dict):
        user_email = self.keycloak.get_user_email(user_id)
        self.logger.info(
            "Notifying user %s about login at %s with fingerprint %s",
            user_id,
            details["Time"],
            details["Fingerprint"],
        )
        if user_email is None:
            self.logger.warn(
                "User %s does not have an email address!", user_id)
            return
        e = mail.Email(user_email, details)
        e.send()

    def notify_new_logins(self):
        if not self.enabled:
            return
        new_logins = session.query(Device).filter(
            Device.is_notified == False).all()
        self.logger.debug(
            "Found %d logins that have no notifications yet", len(new_logins)
        )

        for new_login in new_logins:
            try:
                # Format time with timezone info
                created_at = new_login.created_at
                if hasattr(created_at, 'astimezone'):
                    # Use the timezone and timezone_name set in the constructor
                    localized_time = created_at.astimezone(self.timezone)
                    created_at = f"{localized_time.strftime('%Y-%m-%d %H:%M:%S')} ({self.timezone_name})"
                else:
                    created_at = str(created_at)
                self.notify_user(
                    new_login.user_id,
                    {
                        "Time": created_at,
                        "Device ID": new_login.keycloak_device_id,
                        "Fingerprint": new_login.fingerprint_device_id,
                    },
                )
                self.logger.debug(
                    "Marking user as notified of new device login")
                new_login.is_notified = True
            except KeycloakGetError as e:
                self.logger.warning(
                    "Could not notify user %s about new login. Probably the user has no email.",
                    new_login.user_id,
                )
                self.logger.debug(e)
                # NOTE: we cannot notify users with no email address
                new_login.is_notified = True

        session.commit()
