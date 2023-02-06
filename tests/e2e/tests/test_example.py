from playwright.sync_api import expect


def test_keycloak_home_page(page):
    page.goto("/")
    welcome_heading = page.get_by_role("heading", name="Welcome to Keycloak")
    expect(welcome_heading).to_be_visible()
