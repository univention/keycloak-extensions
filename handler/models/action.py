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
from sqlalchemy import Column, Integer, String, Float, DateTime


class Action(database.Base):
    """
    Action

    Description:
        This table holds actions to prevent brute force attacks, and this can
        be `captcha`, `device` or `IP`, depending on the rules configured. This
        actions will be executed by the proxy and should autoexpire.

    Attributes:
        action (str): `captcha`, `ip`, `device`
        expiration (datetime):
        keycloak_device_id (str):
        fingerprint_device_id (str):
        ip_address (str):
    """

    __tablename__ = 'actions'
    id = Column(Integer, primary_key=True)
    keycloak_device_id = Column(String, nullable=True)
    fingerprint_device_id = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)
    action = Column(String, nullable=False)
    expiration = Column(DateTime, nullable=False)

    def __init__(self, action, expiration, keycloak_device_id=None, fingerprint_device_id=None, ip_address=None):
        assert any([keycloak_device_id, fingerprint_device_id, ip_address])
        self.action = action
        self.expiration = expiration
        self.keycloak_device_id = keycloak_device_id
        self.fingerprint_device_id = fingerprint_device_id
        self.ip_address = ip_address

    def __repr__(self):
        return f"""Action(
            action: {self.action}
            expiration: {self.expiration}
            keycloak_device_id: {self.keycloak_device_id}
            fingerprint_device_id: {self.fingerprint_device_id}
            ip_address: {self.ip_address}
        )"""

    def __str__(self):
        return f"Action({self.keycloak_device_id}, {self.fingerprint_device_id}, {self.ip_address}, {self.action})"
