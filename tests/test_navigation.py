import allure
import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


@allure.feature("Navigation")
class TestNavigation:

    @allure.story("Page title")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.smoke
    def test_page_title(self, page):
        with allure.step("Open login page"):
            login = LoginPage(page)
            login.open()
        with allure.step("Verify page title contains 'Practice'"):
            assert "Practice" in login.get_title()

    @allure.story("Logout")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_logout_redirects_to_login(self, page):
        with allure.step("Login with valid credentials"):
            login = LoginPage(page)
            login.open()
            login.login()
        with allure.step("Click logout"):
            DashboardPage(page).logout()
        with allure.step("Verify redirected back to login URL"):
            assert page.url == login.URL