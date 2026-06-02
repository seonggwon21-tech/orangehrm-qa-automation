import allure
import pytest
from playwright.sync_api import Page, expect

from pages.dashboard_page import DashboardPage


@allure.feature("Dashboard")
class TestDashboard:
    @allure.title("Dashboard heading is visible after login")
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_dashboard_title_visible(self, authenticated_page: Page) -> None:
        DashboardPage(authenticated_page).expect_loaded()

    @allure.title("Sidebar navigation links are present")
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_sidebar_navigation_links_visible(self, authenticated_page: Page) -> None:
        for name in ("Admin", "PIM", "Leave", "Time"):
            locator = authenticated_page.locator(".oxd-main-menu-item").filter(has_text=name)
            expect(locator).to_be_visible()
