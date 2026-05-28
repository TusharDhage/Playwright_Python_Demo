import pytest
import os
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="function")
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        yield page
        context.close()
        browser.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # Only capture on FAILED tests, during the call phase
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            # Create screenshots folder if it doesn't exist
            os.makedirs("reports/screenshots", exist_ok=True)

            # Clean test name for filename
            test_name = item.name.replace("/", "_").replace("::", "_")
            screenshot_path = f"reports/screenshots/{test_name}.png"

            page.screenshot(path=screenshot_path, full_page=True)
            print(f"\nScreenshot saved: {screenshot_path}")