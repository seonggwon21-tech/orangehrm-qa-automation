import allure
import pytest
from playwright.sync_api import Page


# pytest-playwright provides: --browser, --headed, --browser-channel, --slowmo
# --browser chromium|firefox|webkit
# --browser-channel msedge  (use with --browser chromium for Edge)


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
