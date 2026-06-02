import allure
import pytest
from playwright.sync_api import Page

from config.settings import ADMIN_PASSWORD, ADMIN_USERNAME, BASE_URL
from pages.login_page import LoginPage


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        page: Page | None = item.funcargs.get("page")
        if page:
            screenshot = page.screenshot()
            allure.attach(
                screenshot,
                name="screenshot_on_failure",
                attachment_type=allure.attachment_type.PNG,
            )


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    lp = LoginPage(page)
    lp.navigate(BASE_URL)
    return lp


@pytest.fixture
def authenticated_page(page: Page) -> Page:
    lp = LoginPage(page)
    lp.navigate(BASE_URL)
    lp.login(ADMIN_USERNAME, ADMIN_PASSWORD)
    page.wait_for_url("**/dashboard/**")
    return page
