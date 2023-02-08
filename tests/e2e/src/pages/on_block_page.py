import re

from playwright.sync_api import expect

from pages.admin_login_page import AdminLoginPage
from pages.base import BasePage


class OnDeviceBlockPage(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        blocked_msg = re.compile("Too many failed login.*device",
                                 re.IGNORECASE
                                 )
        self.device_blocked_message = self.page.get_by_text(blocked_msg)

    def go_there(self, username, wrong_password, failed_attempts_for_device_block):
        admin_login_page = AdminLoginPage(self.page)
        admin_login_page.go_there()
        for _ in range(failed_attempts_for_device_block):
            admin_login_page.login(username, wrong_password)
            expect(admin_login_page.invalid_login_message).to_be_visible()
        admin_login_page.login(username, wrong_password)
        expect(self.device_blocked_message).to_be_visible()


class OnIPBlockPage(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        blocked_msg = re.compile("Too many failed login.*IP",
                                 re.IGNORECASE
                                 )
        self.ip_blocked_message = self.page.get_by_text(blocked_msg)
