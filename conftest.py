import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
import pytest

API_BASE_URL      = "https://jsonplaceholder.typicode.com"
WIREMOCK_BASE_URL = os.environ.get("WIREMOCK_URL", "http://localhost:8080")
APP_BASE_URL      = os.environ.get("APP_BASE_URL", "https://www.saucedemo.com")

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args,
            "viewport": {"width": 1280, "height": 720},
            "locale": "en-IN", "timezone_id": "Asia/Kolkata",
            "base_url": APP_BASE_URL}

@pytest.fixture(scope="session")
def api_request_context(playwright):
    context = playwright.request.new_context(
        base_url=API_BASE_URL,
        extra_http_headers={"Accept":"application/json","Content-Type":"application/json"})
    yield context
    context.dispose()

@pytest.fixture(scope="session")
def api_base_url():
    return API_BASE_URL

@pytest.fixture(scope="session")
def wiremock_url():
    return WIREMOCK_BASE_URL

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report  = outcome.get_result()
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            import allure
            allure.attach(page.screenshot(full_page=True),
                          name=f"FAILED - {item.name}",
                          attachment_type=allure.attachment_type.PNG)