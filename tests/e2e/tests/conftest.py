import datetime
import os
import tempfile

from playwright.sync_api import expect, Error
import pytest
from slugify import slugify

from pages.admin_login_page import AdminLoginPage


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


@pytest.fixture
def username(pytestconfig):
    return pytestconfig.option.username


@pytest.fixture
def password(pytestconfig):
    return pytestconfig.option.password


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
def wrong_password():
    return "wrong_password"


@pytest.fixture(scope="session")
def playwright(playwright):
    yield playwright
    artifacts_folder.cleanup()


def build_artifact_test_folder(pytestconfig, request, folder_or_file_name):
    output_dir = pytestconfig.getoption("--output")
    return os.path.join(output_dir, slugify(request.node.nodeid), folder_or_file_name)


def agent_page(browser_name, ip):
    @pytest.fixture
    def get_agent_page(playwright, pytestconfig, request):
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
        video = page.video
        if video:
            try:
                video_path = video.path()
                file_name = os.path.basename(video_path)
                video.save_as(
                    path=build_artifact_test_folder(pytestconfig, request, file_name)
                )
            except Error:
                # Silent catch empty videos.
                pass
        browser.close()
    return get_agent_page


agent_chromium_ip_1_page = agent_page("chromium", "127.0.0.12")
agent_firefox_ip_1_page = agent_page("firefox", "127.0.0.12")
agent_chromium_ip_2_page = agent_page("chromium", "127.0.0.13")


# This pattern of defining one fixture per agent doesn't scale.
# Is there a better way?
@pytest.fixture
def agent_chromium_ip_1_login_page(agent_chromium_ip_1_page):
    admin_login_page = AdminLoginPage(agent_chromium_ip_1_page)
    admin_login_page.go_there()


@pytest.fixture
def agent_chromium_ip_2_login_page(agent_chromium_ip_2_page):
    admin_login_page = AdminLoginPage(agent_chromium_ip_2_page)
    admin_login_page.go_there()


@pytest.fixture
def agent_firefox_ip_1_login_page(agent_firefox_ip_1_page):
    admin_login_page = AdminLoginPage(agent_firefox_ip_1_page)
    admin_login_page.go_there()


@pytest.fixture
def agent_chromium_ip_1_trigger_device_block(agent_chromium_ip_1_page,
                                             agent_chromium_ip_1_login_page,
                                             username,
                                             wrong_password,
                                             num_device_block,
                                             release_duration
                                             ):
    this_page = AdminLoginPage(agent_chromium_ip_1_page)
    for _ in range(num_device_block):
        this_page.login(username, wrong_password)
        expect(this_page.invalid_login_message).to_be_visible()
    this_page.login(username, wrong_password)
    block_initiated_at = datetime.datetime.now()
    yield
    now = datetime.datetime.now()
    seconds_since_block = (now - block_initiated_at).total_seconds()
    remaining = max(0, release_duration - seconds_since_block)
    agent_chromium_ip_1_page.wait_for_timeout(round(remaining * 1000) + 1)  # + 1 for safety
    # Consider adding a check here to see if login is actually working
    # Remember: the state here might be logged-in


@pytest.fixture
def trigger_ip_block(agent_chromium_ip_1_page,
                     agent_firefox_ip_1_page,
                     agent_chromium_ip_1_login_page,
                     agent_firefox_ip_1_login_page,
                     username,
                     password,
                     wrong_password,
                     num_device_block,
                     num_ip_block,
                     release_duration
                     ):
    this_page = AdminLoginPage(agent_chromium_ip_1_page)
    for _ in range(num_device_block):
        this_page.login(username, wrong_password)
        expect(this_page.invalid_login_message).to_be_visible()
    this_page = AdminLoginPage(agent_firefox_ip_1_page)
    for _ in range(num_ip_block - num_device_block):
        this_page.login(username, wrong_password)
        expect(this_page.invalid_login_message).to_be_visible()
    this_page.login(username, wrong_password)
    block_initiated_at = datetime.datetime.now()
    yield
    now = datetime.datetime.now()
    seconds_since_block = (now - block_initiated_at).total_seconds()
    remaining = max(0, release_duration - seconds_since_block)
    agent_chromium_ip_1_page.wait_for_timeout(round(remaining * 1000) + 1)  # + 1 for safety
