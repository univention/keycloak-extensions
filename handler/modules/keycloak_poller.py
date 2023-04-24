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

import datetime
import os
import sys
import logging
import time

from modules import mail
from database import session
from models.device import Device

from keycloak import KeycloakAdmin


class KeycloakPoller:

    def __init__(self):
        """
        Initialize KeycloakPoller
        """
        # Configure logging
        log_level = os.environ.get('LOG_LEVEL', 'INFO')
        logging.basicConfig(
            format='%(asctime)s %(levelname)s %(message)s',
            datefmt='%d/%m/%Y %I:%M:%S',
            level=log_level)
        self.logger = logging.getLogger(__name__)

        self.connect()
        self.last_polled_event = None
        self.last_notified_event = None
        self.events = []
        self.retention_period = int(
            os.environ.get("EVENTS_RETENTION_MINUTES", 10))

    def connect(self):
        """
        Connect to Keycloak admin interface
        """
        user_realm_name = os.environ.get("KC_USER_REALM", "")
        if len(user_realm_name) == 0:
            user_realm_name = None

        try:
            self.kc_admin = KeycloakAdmin(
                server_url=os.environ.get("KC_AUTH_URL", None),
                username=os.environ.get("KC_USER", None),
                password=os.environ.get("KC_PASS", None),
                realm_name=os.environ.get("KC_REALM", None),
                user_realm_name=user_realm_name,
                verify=True
            )
        # FIXME: more fine granular exception handling
        except Exception as e:
            self.logger.error("Could not connect to Keycloak")
            self.logger.error(e)
            sys.exit(1)

    def get_new_events(self):
        """
        Get new events from Keycloak
        """
        # See `GET /{realm}/events` at https://www.keycloak.org/docs-api/18.0/rest-api/index.html
        filterDate = {
            # datetime.datetime.now().strftime("%y-%d-%m"),
            "dateFrom": (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
            "dateTo": (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
            "type": ["LOGIN_ERROR"]
        }
        # FIXME: if polling every seconds, we are assuming there will be less than 1k failed login attempts per second (if more, we would lose events)
        last_query_length = 0
        for i in range(1, 100):
            filterDate.update({"max": i * 10})
            try:
                events = self.kc_admin.get_events(filterDate)
            except Exception as e:
                self.logger.debug("Renewing Keycloak connection")
                self.connect()
                events = self.kc_admin.get_events(filterDate)
            if self.last_polled_event in events:
                events = events[:events.index(self.last_polled_event)]
                break
            if last_query_length == len(events):
                break
            last_query_length = len(events)
        self.logger.debug(f"Found {len(events)} unique events in {i} queries")
        if len(events) > 0:
            self.last_polled_event = events[0]
        return events

    def update_events(self):
        """
        Retrieve new events, add them to the state and discard events older than `retention_period`
        """
        new_events = self.get_new_events()
        self.events.extend(new_events)
        self.events = [e for e in self.events if (
            datetime.datetime.now().timestamp() - e["time"]/1000)/60 < self.retention_period]
        return self.events

    def get_user_email(self, user_id):
        user = self.kc_admin.get_user(user_id)
        return user.get("email", None)
