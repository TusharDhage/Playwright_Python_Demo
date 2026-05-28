import pytest
import os
from playwright.sync_api import sync_playwright

def pytest_addoption(parser):
    parser.addoption(
        "--browser-name",
        action="store",
        default="chromium",
        help="Browser to run tests on: chromium, firefox, webkit"
    )

@pytest.fixture(scope="function")
def page(request):
    browser_name = request.config.getoption("--browser-name", default="chromium")

    with sync_playwright() as p:
        # Launch the correct browser based on CLI arg
        browser_map = {
            "chromium": p.chromium,
            "firefox":  p.firefox,
            "webkit":   p.webkit,
        }
        browser = browser_map.get(browser_name, p.chromium).launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        yield page
        context.close()
        browser.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            os.makedirs("reports/screenshots", exist_ok=True)
            test_name = item.name.replace("/", "_").replace("::", "_")
            screenshot_path = f"reports/screenshots/{test_name}.png"
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"\nScreenshot saved: {screenshot_path}")