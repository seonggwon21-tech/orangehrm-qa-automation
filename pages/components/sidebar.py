from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class Sidebar(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._menu = page.locator(".oxd-main-menu-item")

    def _item(self, menu_name: str) -> Locator:
        return self._menu.filter(has=self.page.get_by_text(menu_name, exact=True))

    def navigate_to(self, menu_name: str) -> None:
        self.click(self._item(menu_name))

    def expect_link_visible(self, menu_name: str) -> None:
        self.expect_visible(self._item(menu_name))
