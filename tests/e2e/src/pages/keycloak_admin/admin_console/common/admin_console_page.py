# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2023 Univention GmbH

from pages.base import BasePage
from pages.keycloak_admin.admin_console.common.header import Header


class AdminConsolePage(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.header = Header(self.page.get_by_role("banner"))
