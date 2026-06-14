from playwright.sync_api import Page

from config.settings import DEFAULT_TIMEOUT
from pages.base_page import BasePage
from pages.components.sidebar import Sidebar


class EmployeeListPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.sidebar = Sidebar(page)
        self.table = page.locator(".oxd-table-body")
        self.rows = page.locator(".oxd-table-body .oxd-table-row--clickable")

    def expect_loaded(self) -> None:
        self.wait_for_url("**/pim/viewEmployeeList**")
        self.expect_visible(self.table)

    def get_row_count(self) -> int:
        self.table.wait_for(state="visible", timeout=DEFAULT_TIMEOUT)
        return self.rows.count()
