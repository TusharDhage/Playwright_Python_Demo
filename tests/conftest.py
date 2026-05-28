import pytest
import os
import allure


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

            # Attach screenshot to Allure report
            allure.attach(
                page.screenshot(full_page=True),
                name=f"failure_{test_name}",
                attachment_type=allure.attachment_type.PNG
            )