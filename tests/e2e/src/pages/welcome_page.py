from playwright.sync_api import expect

from pages.base import BasePage


class WelcomePage(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.administrator_console_link = self.page.get_by_role("link", name="Administration Console")

    def click_administrator_console_link(self):
        self.administrator_console_link.click()

    def go_there(self):
        # If logged in, should log out here. Not implemented yet, since we
        # don't have tests for logged in pages yet.
        self.page.goto("/")
        # Checking whether the page looks alright in this place prevents duplication of asserts
        # However, tests concerning this page will need to go to the previous page,
        # navigate here and assert some of the same things
        expect(self.administrator_console_link).to_be_visible()
