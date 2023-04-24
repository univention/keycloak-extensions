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

import time

from modules import keycloak_poller
from modules import action_maker
from modules import notifier
import database

# Import needed for table creation
from models import action
from models import device


if __name__ == "__main__":

    database.Base.metadata.create_all(database.engine)

    keycloak = keycloak_poller.KeycloakPoller()
    action_maker = action_maker.ActionMaker()
    notif = notifier.Notifier(keycloak)

    while True:
        events = keycloak.update_events()
        failed_login_events = [e for e in events if e["type"] == "LOGIN_ERROR"]
        action_maker.remove_expired_actions()
        action_maker.take_actions(failed_login_events)
        notif.notify_new_logins()
        time.sleep(1)
