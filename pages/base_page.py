class BasePage:
    def __init__(self, page):
        self.page = page

    def navigate(self, url):
        self.page.goto(url)

    def get_title(self):
        return self.page.title()

    def click(self, locator):
        self.page.locator(locator).click()

    def fill(self, locator, text):
        self.page.locator(locator).fill(text)

    def get_text(self, locator):
        return self.page.locator(locator).inner_text()

    def is_visible(self, locator):
        return self.page.locator(locator).is_visible()

    def wait_for_url(self, url_pattern):
        self.page.wait_for_url(url_pattern)