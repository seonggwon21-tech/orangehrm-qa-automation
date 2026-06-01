import pytest
from playwright.sync_api import Page, expect

from config.settings import BASE_URL


@pytest.mark.ui
@pytest.mark.smoke
def test_login_page_loads(page: Page) -> None:
    page.goto(BASE_URL)
    expect(page.locator("input[name='username']")).to_be_visible()
    expect(page.locator("input[name='password']")).to_be_visible()
    expect(page.locator("button[type='submit']")).to_be_visible()
