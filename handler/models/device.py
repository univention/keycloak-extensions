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

import database
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, UniqueConstraint
import datetime


class Device(database.Base):
    """
    Device

    Description:
        This table will hold devices with an user attatched, making it easy to track
        new devices login. With this, if a user logs in to a device that it has never
        logged in before, it will be stored here. Also stores if the user was notified
        of the login.

    Attributes:
        keycloak_device_id (str):
        fingerprint_device_id (str):
        user_id (str):
        is_notified (bool):
        created_at (datetime):
    """

    __tablename__ = 'devices'
    __table_args__ = (UniqueConstraint("fingerprint_device_id", "user_id"), )
    id = Column(Integer, primary_key=True)
    keycloak_device_id = Column(String, nullable=False)
    fingerprint_device_id = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    is_notified = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, keycloak_device_id, fingerprint_device_id, user_id, is_notified=False):
        assert any([keycloak_device_id, fingerprint_device_id])
        self.keycloak_device_id = keycloak_device_id
        self.fingerprint_device_id = fingerprint_device_id
        self.user_id = user_id
        self.is_notified = is_notified

    def __repr__(self):
        return f"""Device(
            keycloak_device_id: {self.keycloak_device_id}
            fingerprint_device_id: {self.fingerprint_device_id}
            user_id: {self.user_id}
            is_notified: {self.is_notified}
        )"""

    def __str__(self):
        return f"Device({self.keycloak_device_id}, {self.fingerprint_device_id}, {self.user_id}, {self.is_notified})"
