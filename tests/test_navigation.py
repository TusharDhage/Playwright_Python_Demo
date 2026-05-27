from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

class TestNavigation:

    def test_page_title(self, page):
        login = LoginPage(page)
        login.open()
        assert "Practice" in login.get_title()

    def test_logout_redirects_to_login(self, page):
        login = LoginPage(page)
        login.open()
        login.login("student", "Password123")
        dashboard = DashboardPage(page)
        dashboard.logout()
        assert page.url == login.URL