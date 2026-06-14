from playwright.sync_api import Locator, Page, expect

from config.settings import DEFAULT_TIMEOUT
from utils.logger import get_logger


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.logger = get_logger(self.__class__.__name__)

    def navigate(self, url: str) -> None:
        self.logger.info(f"Navigating to {url}")
        self.page.goto(url)

    def click(self, locator: Locator) -> None:
        locator.wait_for(state="visible", timeout=DEFAULT_TIMEOUT)
        locator.scroll_into_view_if_needed()
        locator.click()

    def fill(self, locator: Locator, value: str) -> None:
        locator.wait_for(state="visible", timeout=DEFAULT_TIMEOUT)
        locator.fill(value)

    def wait_for_url(self, url_pattern: str) -> None:
        self.page.wait_for_url(url_pattern, timeout=DEFAULT_TIMEOUT)

    def expect_visible(self, locator: Locator) -> None:
        expect(locator).to_be_visible(timeout=DEFAULT_TIMEOUT)
