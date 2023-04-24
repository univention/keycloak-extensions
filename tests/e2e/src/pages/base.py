from playwright.sync_api import Locator, Page, expect as playwright_expect


def expect(actual, *args, **kwargs):
    """This method is just like Playwright's expect(), but can also handle page objects and parts"""
    if isinstance(actual, BasePage):
        return playwright_expect(actual.page, *args, **kwargs)
    elif isinstance(actual, BasePagePart):
        return playwright_expect(actual.page_part_locator, *args, **kwargs)
    return playwright_expect(actual, *args, **kwargs)


class PageFactory:
    """Methods common to pages and page parts should go here"""

    def check_its_there(self):
        """Checks that a page or page part is indeed displayed in a playwright Page"""
        raise NotImplementedError


class BasePage(PageFactory):
    """
    All full pages (i.e. which are not page parts) should be derived from this class.
    Methods that are common to full pages, but not page parts, should go here.

    You can do page assertions directly by using expect() from pages.base
    instead of the vanilla expect() supplied by Playwright

    ```
    from pages.base import expect

    class MyPage(BasePage):
        pass

    def some_test(page):
        my_page = MyPage(page)
        my_page.navigate()
        expect(my_page).to_have_title(...)
    ```
    """

    def __init__(self, page: Page):
        self.page = page

    def navigate(self, *args, **kwargs):
        """Should navigate to this page"""
        raise NotImplementedError


class BasePagePart:
    """
    All classes representing page parts should be derived from this class

    The page containing the page part should store a reference to the part page as follows

    ```
    class MyPage(BasePage):
        def __init__(self, page):
            super().__init__(page)
            self.header = Header(self.page.locator(...))
    ```

    Then, you can get do the following:

    ```
    from pages.base import expect

    def some_test(page):
        my_page = MyPage(page)
        expect(my_page.header).is_visible()
    ```
    """

    def __init__(self, page_part_locator):
        if not isinstance(page_part_locator, Locator):
            raise ValueError(
                f"Locators must be of type Locator, got  {type(page_part_locator)}")
        self.page_part_locator = page_part_locator

    def __getattr__(self, name):
        """
        Makes sure playwright locator methods can be directly called on the object
        Use this for checking the page part for visibility etc.

        ```
        my_page.header.is_visible()
        ```
        """
        playwright_locator_attrib = getattr(Locator, name, None)
        if playwright_locator_attrib is None:
            raise AttributeError(
                f"Neither Page Part {self.__class__} nor playwright Locator has attribute {name}")
        return getattr(self.page_part_locator, name)

    def check_its_there(self):
        expect(self).to_be_visible()
