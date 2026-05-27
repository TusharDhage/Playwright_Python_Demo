import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

class TestLogin:

    def test_valid_login(self, page):
        login = LoginPage(page)
        login.open()
        login.login("student", "Password123")
        dashboard = DashboardPage(page)
        assert dashboard.get_heading() == "Logged In Successfully"

    def test_invalid_username(self, page):
        login = LoginPage(page)
        login.open()
        login.login("wronguser", "Password123")
        assert "Your username is invalid!" in login.get_error_message()

    def test_invalid_password(self, page):
        login = LoginPage(page)
        login.open()
        login.login("student", "wrongpass")
        assert "Your password is invalid!" in login.get_error_message()

    def test_empty_credentials(self, page):
        login = LoginPage(page)
        login.open()
        login.login("", "")
        assert login.is_visible("#error")