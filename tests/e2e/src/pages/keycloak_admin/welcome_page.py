from playwright.sync_api import expect

from pages.base import BasePage


class WelcomePage(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.administrator_console_link = self.page.get_by_role(
            "link", name="Administration Console")

    def click_administrator_console_link(self):
        self.administrator_console_link.click()

    def navigate(self):
        self.page.goto("/admin/master/console/")
        account_menu_button = self.page.get_by_role("button", name="admin")
        try:
            # Check if logged in
            expect(account_menu_button).to_be_visible()
        except AssertionError:
            self.page.goto("/")
        else:
            account_menu_button.click()
            account_menu_dropdown = self.page.get_by_role(
                "button", name="admin")
            expect(account_menu_dropdown).to_be_visible()
            account_menu_dropdown.get_by_role(
                "menuitem", name="Sign out").click()
            self.page.goto("/admin/master/console/")
            expect(account_menu_button).to_be_hidden()
            self.page.goto("/")

    def check_its_there(self):
        expect(self.administrator_console_link).to_be_visible()
