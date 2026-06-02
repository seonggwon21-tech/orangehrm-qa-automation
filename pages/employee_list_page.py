from playwright.sync_api import Page, expect

from config.settings import DEFAULT_TIMEOUT
from pages.base_page import BasePage
from pages.components.sidebar import Sidebar


class EmployeeListPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.sidebar = Sidebar(page)
        self.table = page.locator(".oxd-table-body")
        self.rows = page.locator(".oxd-table-body .oxd-table-row--clickable")
        self.search_button = page.get_by_role("button", name="Search")

    def expect_loaded(self) -> None:
        self.page.wait_for_url("**/pim/viewEmployeeList**", timeout=DEFAULT_TIMEOUT)
        expect(self.table).to_be_visible(timeout=DEFAULT_TIMEOUT)

    def get_row_count(self) -> int:
        self.rows.first.wait_for(state="visible", timeout=DEFAULT_TIMEOUT)
        return self.rows.count()
