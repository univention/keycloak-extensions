# Like what you see? Join us!
# https://www.univention.com/about-us/careers/vacancies/
#
# Copyright 2020-2023 Univention GmbH
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
import smtplib
import socket
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib.parse import urlparse

DEFAULT_SUBJECT = "Recent sign-in to a Nubus account on {fqdn}"

BODY_TEMPLATE = """Information about recent account activity

A sign-in to the following Nubus account was registered from a device or
browser that has not been used for this account before.

  Account:   {full_name}
  E-mail:    {email}
  Instance:  {fqdn}
  Time:      {time}

No action is required if this sign-in is known and expected.

If this sign-in is unknown, the password of the account should be changed
immediately and the administrator of this Nubus instance should be informed.

This message was sent automatically by Nubus at {fqdn}.

--
Reference for administrators:
  Device ID: {device_id}
"""


def get_instance_fqdn():
    """
    Public FQDN of the Nubus instance shown in the notification.

    Uses `INSTANCE_FQDN` and falls back to the host name of `KC_AUTH_URL`.
    """
    fqdn = os.environ.get("INSTANCE_FQDN", "").strip()
    if fqdn:
        return fqdn
    return urlparse(os.environ.get("KC_AUTH_URL", "")).hostname or ""


def render_subject(template, fqdn):
    """
    Substitute `{fqdn}` in the configured subject.

    A subject with other or unbalanced braces is used verbatim, so that a
    custom subject never prevents the notification from being sent.
    """
    try:
        return template.format(fqdn=fqdn)
    except (KeyError, IndexError, ValueError):
        return template


class Email:
    def __init__(self, receiver, details):
        """
        :param receiver: email address of the user
        :param details: dict with the keys `full_name`, `time` and `device_id`
        """
        self.receiver = receiver
        self.fqdn = get_instance_fqdn()
        self.message = MIMEMultipart()
        self.message["To"] = receiver
        self.message["Subject"] = render_subject(
            os.environ.get("NEW_DEVICE_LOGIN_SUBJECT") or DEFAULT_SUBJECT,
            self.fqdn,
        )
        self.message["From"] = os.environ.get("MAIL_FROM", None)
        self.generate_body(details)
        self.sender = os.environ.get("MAIL_FROM", None)
        self.smtp_user = os.environ.get("SMTP_USERNAME", None)
        self.smtp_pass = os.environ.get("SMTP_PASSWORD", None)
        self.smtp_auth_enabled = (
            os.environ.get("SMTP_AUTH_ENABLED", "true").lower() == "true"
        )
        assert self.sender is not None
        if self.smtp_auth_enabled:
            assert self.smtp_user is not None
            assert self.smtp_pass is not None
        self.smtp_host = os.environ.get("SMTP_HOST", None)
        self.smtp_port = int(os.environ.get("SMTP_PORT", 587))
        self.smtp_ssl = os.environ.get(
            "SMTP_SSL_ENABLED", "false").lower() == "true"
        self.smtp_starttls = (
            os.environ.get("SMTP_STARTTLS_ENABLED", "true").lower() == "true"
        )

        # Configure logging
        log_level = os.environ.get("LOG_LEVEL", "INFO")
        logging.basicConfig(
            format="%(asctime)s %(levelname)s %(message)s",
            datefmt="%d/%m/%Y %I:%M:%S",
            level=log_level,
        )
        self.logger = logging.getLogger(__name__)

    def generate_body(self, details: dict):
        body = BODY_TEMPLATE.format(
            full_name=details["full_name"],
            email=self.receiver,
            fqdn=self.fqdn,
            time=details["time"],
            device_id=details["device_id"],
        )
        self.message.attach(MIMEText(body, "plain", "utf-8"))

    def send(self):
        self.logger.debug(f"Sending email to {self.receiver}")
        context = ssl.create_default_context()

        try:
            if self.smtp_ssl:
                server = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port)
            else:
                server = smtplib.SMTP(self.smtp_host, self.smtp_port)

            with server:
                server.ehlo()
                if self.smtp_starttls and not self.smtp_ssl:
                    server.starttls(context=context)
                    server.ehlo()
                if self.smtp_auth_enabled:
                    server.login(self.smtp_user, self.smtp_pass)
                server.sendmail(self.sender, self.receiver,
                                self.message.as_string())
            self.logger.debug("Successfully sent email to %s", self.receiver)
        except ConnectionRefusedError:
            self.logger.error(
                "Connection to mailserver %s refused", self.smtp_host)
        except socket.gaierror:
            self.logger.error(
                "Hostname resolution failed. Check SMTP host address.")
        except Exception as e:
            self.logger.error(
                "An unexpected error occurred while sending the email: %s", e
            )
