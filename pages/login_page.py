from playwright.sync_api import Page, expect

from config.settings import DEFAULT_TIMEOUT
from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.username_input = page.get_by_placeholder("Username")
        self.password_input = page.get_by_placeholder("Password")
        self.submit_button = page.get_by_role("button", name="Login")
        self.error_alert = page.locator(".oxd-alert-content-text")
        self.field_errors = page.locator(".oxd-input-field-error-message")

    def login(self, username: str, password: str) -> None:
        self.fill(self.username_input, username)
        self.fill(self.password_input, password)
        self.click(self.submit_button)

    def expect_error(self, text: str) -> None:
        expect(self.error_alert).to_have_text(text, timeout=DEFAULT_TIMEOUT)

    def expect_field_required(self, count: int) -> None:
        expect(self.field_errors).to_have_text(["Required"] * count, timeout=DEFAULT_TIMEOUT)
