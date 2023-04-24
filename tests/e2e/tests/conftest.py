import datetime
import os
import tempfile

from playwright.sync_api import expect, Error
import pytest
from slugify import slugify

from pages.keycloak_admin.admin_login_page import AdminLoginPage


artifacts_folder = tempfile.TemporaryDirectory(prefix="playwright-pytest-")


def pytest_addoption(parser):
    parser.addoption("--username", default="admin",
                     help="Keycloak admin login username"
                     )
    parser.addoption("--password", default="univention",
                     help="Keycloak admin login password"
                     )
    parser.addoption("--num-device-block", type=int, default=5,
                     help="Number of failed logins for device block"
                     )
    parser.addoption("--num-ip-block", type=int, default=7,
                     help="Number of failed logins for IP block"
                     )
    parser.addoption("--release-duration", type=int, default=60,
                     help="Blocks are released after this many seconds"
                     )
    parser.addoption("--realm", default="master",
                     help="Realm to attempt logins at"
                     )


@pytest.fixture
def username(pytestconfig):
    return pytestconfig.option.username


@pytest.fixture
def password(pytestconfig):
    return pytestconfig.option.password


@pytest.fixture
def realm(pytestconfig):
    return pytestconfig.option.realm


@pytest.fixture(scope="session")
def base_url(pytestconfig):
    return pytestconfig.getoption("--base-url")


@pytest.fixture
def num_device_block(pytestconfig):
    return pytestconfig.getoption("--num-device-block")


@pytest.fixture
def num_ip_block(pytestconfig):
    return pytestconfig.getoption("--num-ip-block")


@pytest.fixture
def release_duration(pytestconfig):
    return pytestconfig.getoption("--release-duration")


@pytest.fixture
def wrong_password(pytestconfig):
    return pytestconfig.option.password + "wrong_password"


@pytest.fixture(scope="session")
def playwright(playwright):
    yield playwright
    artifacts_folder.cleanup()


def build_artifact_test_folder(pytestconfig, request, folder_or_file_name):
    output_dir = pytestconfig.getoption("--output")
    return os.path.join(output_dir, slugify(request.node.nodeid), folder_or_file_name)


def get_page(browser_name, ip):
    @pytest.fixture
    def get_page_for_browser_and_ip(playwright, pytestconfig, request):
        browser_type = getattr(playwright, browser_name)
        launch_options = {}
        headed_option = pytestconfig.getoption("--headed")
        if headed_option:
            launch_options["headless"] = False
        slowmo_option = pytestconfig.getoption("--slowmo")
        if slowmo_option:
            launch_options["slow_mo"] = slowmo_option
        browser = browser_type.launch(**launch_options)
        browser_context_args = {}
        base_url = pytestconfig.getoption("--base-url")
        if base_url:
            browser_context_args["base_url"] = base_url
        video_option = pytestconfig.getoption("--video")
        capture_video = video_option in ["on", "retain-on-failure"]
        if capture_video:
            browser_context_args["record_video_dir"] = artifacts_folder.name
        browser_context = browser.new_context(**browser_context_args)
        browser_context.set_extra_http_headers({"X-Forwarded-For": ip})
        page = browser_context.new_page()
        yield page
        browser_context.close()
        video_option = pytestconfig.getoption("--video")
        failed = request.node.rep_call.failed if hasattr(
            request.node, "rep_call") else True
        preserve_video = video_option == "on" or (
            failed and video_option == "retain-on-failure"
        )
        if preserve_video:
            video = page.video
            if video:
                try:
                    video_path = video.path()
                    file_name = os.path.basename(video_path)
                    video.save_as(
                        path=build_artifact_test_folder(
                            pytestconfig, request, file_name)
                    )
                except Error:
                    # Silent catch empty videos.
                    pass
        browser.close()
    return get_page_for_browser_and_ip


chromium_ip_1_page = get_page("chromium", "127.0.0.12")
firefox_ip_1_page = get_page("firefox", "127.0.0.12")
chromium_ip_2_page = get_page("chromium", "127.0.0.13")


@pytest.fixture
def navigate_to_login_page_chromium_ip_1(chromium_ip_1_page):
    admin_login_page = AdminLoginPage(chromium_ip_1_page)
    admin_login_page.navigate()
    return chromium_ip_1_page


@pytest.fixture
def navigate_to_login_page_chromium_ip_2(chromium_ip_2_page):
    admin_login_page = AdminLoginPage(chromium_ip_2_page)
    admin_login_page.navigate()
    return chromium_ip_2_page


@pytest.fixture
def navigate_to_login_page_firefox_ip_1(firefox_ip_1_page):
    admin_login_page = AdminLoginPage(firefox_ip_1_page)
    admin_login_page.navigate()
    return firefox_ip_1_page


@pytest.fixture
def trigger_device_block_chromium_ip_1(navigate_to_login_page_chromium_ip_1,
                                       username,
                                       wrong_password,
                                       num_device_block,
                                       release_duration
                                       ):
    page = navigate_to_login_page_chromium_ip_1
    login_page = AdminLoginPage(page)
    for _ in range(num_device_block):
        login_page.login(username, wrong_password)
        expect(login_page.invalid_login_message).to_be_visible()
    login_page.login(username, wrong_password)
    block_initiated_at = datetime.datetime.now()
    yield page
    now = datetime.datetime.now()
    seconds_since_block = (now - block_initiated_at).total_seconds()
    remaining = max(0, release_duration - seconds_since_block)
    page.wait_for_timeout(round(remaining * 1000) + 1)  # + 1 for safety
    # Consider adding a check here to see if login is actually working
    # Remember: the state here might be logged-in


@pytest.fixture
def trigger_ip_block(navigate_to_login_page_chromium_ip_1,
                     navigate_to_login_page_firefox_ip_1,
                     username,
                     password,
                     wrong_password,
                     num_device_block,
                     num_ip_block,
                     release_duration
                     ):
    chromium_ip_1_page = navigate_to_login_page_chromium_ip_1
    login_page = AdminLoginPage(chromium_ip_1_page)
    for _ in range(num_device_block):
        login_page.login(username, wrong_password)
        expect(login_page.invalid_login_message).to_be_visible()

    firefox_ip_1_page = navigate_to_login_page_firefox_ip_1
    login_page = AdminLoginPage(firefox_ip_1_page)
    for _ in range(num_ip_block - num_device_block):
        login_page.login(username, wrong_password)
        expect(login_page.invalid_login_message).to_be_visible()
    login_page.login(username, wrong_password)
    block_initiated_at = datetime.datetime.now()
    yield chromium_ip_1_page, firefox_ip_1_page
    now = datetime.datetime.now()
    seconds_since_block = (now - block_initiated_at).total_seconds()
    remaining = max(0, release_duration - seconds_since_block)
    chromium_ip_1_page.wait_for_timeout(
        round(remaining * 1000) + 1)  # + 1 for safety
