import pytest
import allure
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utils.config import Config


@allure.feature("Login")
class TestLogin:

    @allure.story("Valid login")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.login
    def test_valid_login(self, page):
        with allure.step("Open login page"):
            login = LoginPage(page)
            login.open()
        with allure.step("Enter valid credentials and submit"):
            login.login()
        with allure.step("Verify dashboard heading"):
            assert DashboardPage(page).get_heading() == "Logged In Successfully"

    @allure.story("Invalid login")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.login
    def test_invalid_username(self, page):
        with allure.step("Open login page"):
            login = LoginPage(page)
            login.open()
        with allure.step("Enter invalid username"):
            login.login("wronguser", Config.PASSWORD)
        with allure.step("Verify error message"):
            assert "Your username is invalid!" in login.get_error_message()

    @allure.story("Invalid login")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.login
    def test_invalid_password(self, page):
        with allure.step("Open login page"):
            login = LoginPage(page)
            login.open()
        with allure.step("Enter invalid password"):
            login.login(Config.USERNAME, "wrongpass")
        with allure.step("Verify error message"):
            assert "Your password is invalid!" in login.get_error_message()

    @allure.story("Invalid login")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    @pytest.mark.login
    @pytest.mark.parametrize("username,password,expected_error", [
        ("wronguser", "Password123", "Your username is invalid!"),
        ("student",   "wrongpass",   "Your password is invalid!"),
        ("",          "",            "Your username is invalid!"),
    ])
    def test_invalid_login_scenarios(self, page, username, password, expected_error):
        with allure.step(f"Login with username='{username}'"):
            login = LoginPage(page)
            login.open()
            login.login(username, password)
        with allure.step("Verify error message"):
            assert expected_error in login.get_error_message()