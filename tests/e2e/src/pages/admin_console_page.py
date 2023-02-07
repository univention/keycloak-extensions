from playwright.sync_api import expect

from pages.admin_login_page import AdminLoginPage
from pages.base import BasePage


class AdminConsolePage(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.realm_selector = self.page.get_by_test_id("realmSelectorToggle")

    def go_there(self, username, password):
        admin_login_page = AdminLoginPage(self.page)
        admin_login_page.go_there()
        admin_login_page.login(username, password)
        expect(self.realm_selector).to_be_visible()
