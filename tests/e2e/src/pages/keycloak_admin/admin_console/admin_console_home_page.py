from pages.base import expect
from pages.keycloak_admin.admin_console.common.admin_console_page import AdminConsolePage
from pages.keycloak_admin.admin_login_page import AdminLoginPage


class AdminConsoleHomePage(AdminConsolePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.realm_selector = self.page.get_by_test_id("realmSelectorToggle")

    def navigate(self, username, password):
        # this page is the canonical navigation root for logged in pages, so using URL to navigate
        self.page.goto("/admin/master/console/")
        try:
            # Check if logged in
            expect(self.header.account_menu_dropdown).to_be_visible()
        except AssertionError:
            admin_login_page = AdminLoginPage(self.page)
            admin_login_page.navigate()
            admin_login_page.check_its_there()
            admin_login_page.login(username, password)

    def check_its_there(self):
        expect(self.realm_selector).to_be_visible()
