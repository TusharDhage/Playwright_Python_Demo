from pages.base_page import BasePage
from utils.config import Config

class LoginPage(BasePage):
    URL = Config.BASE_URL

    # Locators
    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON   = "#submit"
    ERROR_MESSAGE  = "#error"
    SUCCESS_TEXT   = ".post-title"

    def open(self):
        self.navigate(self.URL)

    def login(self, username=None, password=None):
        # Use config defaults if no args passed
        username = username or Config.USERNAME
        password = password or Config.PASSWORD
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self):
        return self.get_text(self.ERROR_MESSAGE)

    def is_login_successful(self):
        return self.is_visible(self.SUCCESS_TEXT)