import pytest

from pages.login_page import LoginPage


@pytest.mark.ui
@pytest.mark.smoke
def test_login_page_loads(login_page: LoginPage) -> None:
    login_page.expect_loaded()
