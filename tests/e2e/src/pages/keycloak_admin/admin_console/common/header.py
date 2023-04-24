from pages.base import BasePagePart, expect


class Header(BasePagePart):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.account_menu_button = self.get_by_role("button", name="admin")
        self.account_menu_dropdown = AccountMenuDropdown(
            self.get_by_role("menu", name="admin"))

    def check_its_there(self):
        expect(self.account_menu_button).to_be_visible()

    def click_account_menu_button(self):
        self.account_menu_button.click()

    def logout(self):
        self.click_account_menu_button()
        expect(self.account_menu_dropdown).to_be_visible()
        self.account_menu_dropdown.click_sign_out_button()


class AccountMenuDropdown(BasePagePart):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sign_out_button = self.get_by_role("menuitem", name="Sign out")

    def click_sign_out_button(self):
        self.sign_out_button.click()

    def check_its_there(self):
        expect(self.sign_out_button).to_be_visible()
