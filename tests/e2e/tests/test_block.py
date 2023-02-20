from playwright.sync_api import expect

from pages.admin_console_page import AdminConsolePage, AdminLoginPage
from pages.on_block_page import OnDeviceBlockPage, OnIPBlockPage


def test_device_block(agent_chromium_ip_1_page,
                      agent_firefox_ip_1_page,
                      agent_chromium_ip_1_trigger_device_block,
                      agent_firefox_ip_1_login_page,
                      username,
                      password,
                      release_duration
                      ):
    admin_login_page = AdminLoginPage(agent_chromium_ip_1_page)
    expect(admin_login_page.invalid_login_message).to_be_hidden()
    on_device_block_page = OnDeviceBlockPage(agent_chromium_ip_1_page)
    expect(on_device_block_page.device_blocked_message).to_be_visible()

    admin_login_page = AdminLoginPage(agent_firefox_ip_1_page)
    admin_login_page.login(username, password)
    admin_console_page = AdminConsolePage(agent_firefox_ip_1_page)
    expect(admin_console_page.realm_selector).to_be_visible()

    agent_chromium_ip_1_page.wait_for_timeout(round(release_duration * 1000) + 1)  # + 1 for safety
    admin_console_page = AdminConsolePage(agent_chromium_ip_1_page)
    admin_console_page.go_there(username, password)


def test_ip_block(agent_firefox_ip_1_page,
                  agent_chromium_ip_2_page,
                  trigger_ip_block,
                  agent_chromium_ip_2_login_page,
                  username,
                  password,
                  release_duration
                  ):
    admin_login_page = AdminLoginPage(agent_firefox_ip_1_page)
    expect(admin_login_page.invalid_login_message).to_be_hidden()
    on_ip_block_page = OnIPBlockPage(agent_firefox_ip_1_page)
    expect(on_ip_block_page.ip_blocked_message).to_be_visible()

    admin_login_page = AdminLoginPage(agent_chromium_ip_2_page)
    admin_login_page.login(username, password)
    admin_console_page = AdminConsolePage(agent_chromium_ip_2_page)
    expect(admin_console_page.realm_selector).to_be_visible()

    agent_firefox_ip_1_page.wait_for_timeout(round(release_duration * 1000) + 1)  # + 1 for safety
    admin_console_page = AdminConsolePage(agent_firefox_ip_1_page)
    admin_console_page.go_there(username, password)
