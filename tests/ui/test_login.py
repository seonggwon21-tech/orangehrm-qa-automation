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

    @allure.title("Wrong credentials show 'Invalid credentials': {case_id}")
    @pytest.mark.ui
    @pytest.mark.regression
    @pytest.mark.parametrize(
        ("case_id", "username", "password"),
        [
            ("wrong_password", ADMIN_USERNAME, "wrong_password"),
            ("wrong_username", "wrong_user", ADMIN_PASSWORD),
            ("both_wrong", "wrong_user", "wrong_password"),
        ],
    )
    def test_login_with_invalid_credentials(
        self, login_page: LoginPage, case_id: str, username: str, password: str
    ) -> None:
        login_page.login(username, password)
        login_page.expect_error("Invalid credentials")

    @allure.title("Empty fields show 'Required' validation: {case_id}")
    @pytest.mark.ui
    @pytest.mark.regression
    @pytest.mark.parametrize(
        ("case_id", "username", "password", "expected_errors"),
        [
            ("empty_username", "", ADMIN_PASSWORD, 1),
            ("empty_password", ADMIN_USERNAME, "", 1),
            ("both_empty", "", "", 2),
        ],
    )
    def test_login_with_empty_fields(
        self,
        login_page: LoginPage,
        case_id: str,
        username: str,
        password: str,
        expected_errors: int,
    ) -> None:
        login_page.login(username, password)
        login_page.expect_field_required(expected_errors)
