import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

class TestLogin:

    @pytest.mark.smoke
    @pytest.mark.login
    def test_valid_login(self, page):
        login = LoginPage(page)
        login.open()
        login.login("student", "Password123")
        assert DashboardPage(page).get_heading() == "Logged In Successfully"

    @pytest.mark.regression
    @pytest.mark.login
    def test_invalid_username(self, page):
        login = LoginPage(page)
        login.open()
        login.login("wronguser", "Password123")
        assert "Your username is invalid!" in login.get_error_message()

    @pytest.mark.regression
    @pytest.mark.login
    def test_invalid_password(self, page):
        login = LoginPage(page)
        login.open()
        login.login("student", "wrongpass")
        assert "Your password is invalid!" in login.get_error_message()

    @pytest.mark.regression
    @pytest.mark.login
    def test_empty_credentials(self, page):
        login = LoginPage(page)
        login.open()
        login.login("", "")
        assert login.is_visible("#error")

    @pytest.mark.regression
    @pytest.mark.login
    @pytest.mark.parametrize("username, password, expected_error", [
        ("wronguser", "Password123", "Your username is invalid!"),
        ("student", "wrongpass", "Your password is invalid!"),
        ("", "", "Your username is invalid!"),
        ("wronguser", "", "Your username is invalid!"),
    ])
    def test_invalid_login_scenarios(self, page, username, password, expected_error):
        login = LoginPage(page)
        login.open()
        login.login(username, password)
        assert expected_error in login.get_error_message()