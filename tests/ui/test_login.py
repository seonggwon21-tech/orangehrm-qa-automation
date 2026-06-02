import allure
import pytest

from config.settings import ADMIN_PASSWORD, ADMIN_USERNAME
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage


@allure.feature("Authentication")
class TestLogin:
    @allure.title("Valid credentials redirect to dashboard")
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_login_with_valid_credentials(self, login_page: LoginPage) -> None:
        login_page.login(ADMIN_USERNAME, ADMIN_PASSWORD)
        DashboardPage(login_page.page).expect_loaded()

    @allure.title("Invalid password shows error message")
    @pytest.mark.ui
    @pytest.mark.regression
    def test_login_with_invalid_password(self, login_page: LoginPage) -> None:
        login_page.login(ADMIN_USERNAME, "wrong_password")
        login_page.expect_error("Invalid credentials")
