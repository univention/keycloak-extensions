import requests
from time import sleep
from playwright.sync_api import expect

from pages.keycloak_admin.admin_console.admin_console_home_page import AdminConsoleHomePage
from pages.keycloak_admin.admin_login_page import AdminLoginPage
from pages.keycloak_admin.on_block_page import OnDeviceBlockPage, OnIPBlockPage

from api.keycloak_api import KeycloakAPI


def test_device_block(trigger_device_block_chromium_ip_1,
                      navigate_to_login_page_firefox_ip_1,
                      username,
                      password,
                      release_duration
                      ):
    # TODO: parametrize realm
    chromium_ip_1_page = trigger_device_block_chromium_ip_1
    firefox_ip_1_page = navigate_to_login_page_firefox_ip_1

    admin_login_page = AdminLoginPage(chromium_ip_1_page)
    expect(admin_login_page.invalid_login_message).to_be_hidden()
    on_device_block_page = OnDeviceBlockPage(chromium_ip_1_page)
    expect(on_device_block_page.device_blocked_message).to_be_visible()

    admin_login_page = AdminLoginPage(firefox_ip_1_page)
    admin_login_page.check_its_there()
    admin_login_page.login(username, password)
    admin_console_home_page = AdminConsoleHomePage(firefox_ip_1_page)
    admin_console_home_page.check_its_there()

    chromium_ip_1_page.wait_for_timeout(round(release_duration * 1000) + 1)  # + 1 for safety
    admin_console_home_page = AdminConsoleHomePage(chromium_ip_1_page)
    admin_console_home_page.navigate(username, password)
    admin_console_home_page.check_its_there()


def test_ip_block(trigger_ip_block,
                  navigate_to_login_page_chromium_ip_2,
                  username,
                  password,
                  release_duration
                  ):
    # TODO: parametrize realm
    chromium_ip_1_page, firefox_ip_1_page = trigger_ip_block
    chromium_ip_2_page = navigate_to_login_page_chromium_ip_2

    admin_login_page = AdminLoginPage(firefox_ip_1_page)
    expect(admin_login_page.invalid_login_message).to_be_hidden()
    on_ip_block_page = OnIPBlockPage(firefox_ip_1_page)
    on_ip_block_page.check_its_there()

    admin_login_page = AdminLoginPage(chromium_ip_2_page)
    admin_login_page.check_its_there()
    admin_login_page.login(username, password)
    admin_console_home_page = AdminConsoleHomePage(chromium_ip_2_page)
    admin_console_home_page.check_its_there()

    firefox_ip_1_page.wait_for_timeout(round(release_duration * 1000) + 1)  # + 1 for safety
    admin_console_home_page = AdminConsoleHomePage(firefox_ip_1_page)
    admin_console_home_page.navigate(username, password)
    admin_console_home_page.check_its_there()


def test_api_ip_block(num_ip_block, username, password, wrong_password, realm, release_duration, base_url):
    # Generate docstring for this function
    kc_api = KeycloakAPI(base_url, realm)
    r = kc_api.get_oidc_token(username, password)
    assert r.status_code == 200
    assert r.json()["access_token"] is not None
    for _ in range(num_ip_block):
        r = kc_api.get_oidc_token(username, wrong_password)
        assert r.status_code == 401
    # Allow ~1 second for the handler to retrieve the logins and evaluate actions
    sleep(2)
    r = kc_api.get_oidc_token(username, password)
    assert r.status_code == 429
    assert r.text == "Too many failed login attempts on this IP. Wait for cooldown."
    # Allow handler to remove expired actions
    sleep(release_duration + 1)
    r = kc_api.get_oidc_token(username, password)
    assert r.status_code == 200
    assert r.json()["access_token"] is not None

