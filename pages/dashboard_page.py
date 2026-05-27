from pages.base_page import BasePage

class DashboardPage(BasePage):
    SUCCESS_HEADING = ".post-title"
    LOGOUT_BUTTON   = ".wp-block-button a"

    def get_heading(self):
        return self.get_text(self.SUCCESS_HEADING)

    def logout(self):
        self.click(self.LOGOUT_BUTTON)