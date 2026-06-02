from playwright.sync_api import Page

from pages.base_page import BasePage


class Sidebar(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._menu = page.locator(".oxd-main-menu-item")

    def navigate_to(self, menu_name: str) -> None:
        self.click(self._menu.filter(has_text=menu_name))

    def expect_link_visible(self, menu_name: str) -> None:
        self.expect_visible(self._menu.filter(has_text=menu_name))
