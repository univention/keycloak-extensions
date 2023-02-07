from playwright.sync_api import expect

from pages.base import BasePage
from pages.welcome_page import WelcomePage


class AdminLoginPage(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username_input = self.page.get_by_label("Username or email")
        self.password_input = self.page.get_by_label("Password")
        self.submit_button = self.page.get_by_role("button", name="Sign In")
        self.invalid_login_message = self.page.get_by_text("Invalid username or password.")

    def go_there(self):
        welcome_page = WelcomePage(self.page)
        welcome_page.go_there()
        welcome_page.click_administrator_console_link()
        expect(self.username_input).to_be_visible()
        expect(self.password_input).to_be_visible()
        expect(self.submit_button).to_be_visible()

    def fill_username(self, username):
        self.username_input.fill(username)

    def fill_password(self, password):
        self.password_input.fill(password)

    def click_submit_button(self):
        self.submit_button.click()

    def login(self, username, password):
        self.fill_username(username)
        self.fill_password(password)
        self.click_submit_button()
