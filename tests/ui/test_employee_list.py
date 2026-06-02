import allure
import pytest
from playwright.sync_api import Page

from pages.employee_list_page import EmployeeListPage


@allure.feature("Employee Management")
class TestEmployeeList:
    @allure.title("Employee list table loads after navigating to PIM")
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_employee_list_loads(self, authenticated_page: Page) -> None:
        emp = EmployeeListPage(authenticated_page)
        emp.sidebar.navigate_to("PIM")
        emp.expect_loaded()
        assert emp.get_row_count() > 0
