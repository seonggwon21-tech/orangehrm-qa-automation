from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.components.sidebar import Sidebar


class DashboardPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.sidebar = Sidebar(page)
        self.heading = page.get_by_role("heading", name="Dashboard")

    def expect_loaded(self) -> None:
        self.wait_for_url("**/dashboard/**")
        self.expect_visible(self.heading)
