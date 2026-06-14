from playwright.sync_api import Page, expect

from config.settings import DEFAULT_TIMEOUT
from pages.base_page import BasePage
from pages.components.sidebar import Sidebar


class DashboardPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.sidebar = Sidebar(page)
        self.heading = page.get_by_role("heading", name="Dashboard")

    def expect_loaded(self) -> None:
        self.wait_for_url("**/dashboard/**")
        expect(self.heading).to_be_visible(timeout=DEFAULT_TIMEOUT)
