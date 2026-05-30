import os
import pytest
import allure
from typing import Generator
from playwright.sync_api import sync_playwright, Page, BrowserContext, ViewportSize


MOBILE_DEVICES = [
    "iPhone 13",
    "iPhone SE",
    "Pixel 5",
    "Galaxy S8",
    "iPad (gen 7)",
]


@pytest.fixture
def mobile_page(request, browser_type_launch_args) -> Generator[tuple[Page, str], None, None]:
    """Fixture that respects --headed and --slowmo flags"""
    device_name: str = request.param
    with sync_playwright() as p:
        # browser_type_launch_args contains headed/slowmo from CLI
        browser = p.chromium.launch(**browser_type_launch_args)
        device = p.devices[device_name]
        viewport: ViewportSize = device.get("viewport")
        context: BrowserContext = browser.new_context(
            viewport=viewport,
            user_agent=device.get("user_agent"),
            has_touch=device.get("has_touch", False),
            is_mobile=device.get("is_mobile", False),
            device_scale_factor=device.get("device_scale_factor", 1),
        )
        page: Page = context.new_page()
        yield page, device_name
        context.close()
        browser.close()


@pytest.fixture
def custom_viewport_page(request, browser_type_launch_args) -> Generator[tuple[Page, str], None, None]:
    """Fixture for custom viewport — respects --headed and --slowmo"""
    width: int
    height: int
    width, height = request.param
    with sync_playwright() as p:
        browser = p.chromium.launch(**browser_type_launch_args)
        viewport: ViewportSize = {"width": width, "height": height}
        context: BrowserContext = browser.new_context(
            viewport=viewport
        )
        page: Page = context.new_page()
        yield page, f"{width}x{height}"
        context.close()
        browser.close()

@allure.feature("Mobile Viewport")
class TestMobileDevices:

    @allure.story("Mobile page load")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.mobile
    @pytest.mark.parametrize("mobile_page", MOBILE_DEVICES, indirect=True)
    def test_login_page_loads_on_mobile(self, mobile_page: tuple[Page, str]):
        page, device_name = mobile_page
        with allure.step(f"Open login page on {device_name}"):
            page.goto(
                "https://practicetestautomation.com/practice-test-login/"
            )
        with allure.step("Verify page title"):
            assert "Practice" in page.title()
        with allure.step("Verify login form visible"):
            assert page.locator("#username").is_visible()
            assert page.locator("#password").is_visible()
            assert page.locator("#submit").is_visible()
        with allure.step(f"Take screenshot on {device_name}"):
            os.makedirs("reports/screenshots/mobile", exist_ok=True)
            page.screenshot(
                path=f"reports/screenshots/mobile/{device_name.replace(' ', '_')}.png",
                full_page=True
            )

    @allure.story("Mobile login flow")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.mobile
    @pytest.mark.parametrize("mobile_page", ["iPhone 13", "Pixel 5"], indirect=True)
    def test_login_works_on_mobile(self, mobile_page: tuple[Page, str]):
        page, device_name = mobile_page
        with allure.step(f"Open login page on {device_name}"):
            page.goto(
                "https://practicetestautomation.com/practice-test-login/"
            )
        with allure.step("Enter credentials"):
            page.locator("#username").fill("student")
            page.locator("#password").fill("Password123")
            page.locator("#submit").click()
        with allure.step("Verify successful login"):
            assert page.locator(".post-title").is_visible()
            assert "Logged In Successfully" in \
                   page.locator(".post-title").inner_text()

    @allure.story("Viewport size check")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    @pytest.mark.mobile
    @pytest.mark.parametrize("mobile_page", MOBILE_DEVICES, indirect=True)
    def test_correct_viewport_applied(self, mobile_page: tuple[Page, str]):
        page, device_name = mobile_page
        with allure.step(f"Open page on {device_name}"):
            page.goto(
                "https://practicetestautomation.com/practice-test-login/"
            )
        with allure.step("Verify viewport is mobile sized"):
            viewport = page.viewport_size
            assert viewport["width"] <= 1024, \
                f"Expected mobile width, got {viewport['width']}"


@allure.feature("Custom Viewport")
class TestCustomViewports:

    @allure.story("Responsive layout")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.mobile
    @pytest.mark.parametrize("custom_viewport_page", [
        (375, 667),
        (390, 844),
        (768, 1024),
        (1280, 720),
        (1920, 1080),
    ], indirect=True)
    def test_page_loads_on_custom_viewport(
        self, custom_viewport_page: tuple[Page, str]
    ):
        page, size = custom_viewport_page
        with allure.step(f"Open page at {size}"):
            page.goto(
                "https://practicetestautomation.com/practice-test-login/"
            )
        with allure.step("Verify page loaded"):
            assert page.locator("#username").is_visible()
        with allure.step("Take screenshot"):
            os.makedirs("reports/screenshots/viewports", exist_ok=True)
            page.screenshot(
                path=f"reports/screenshots/viewports/viewport_{size}.png",
                full_page=True
            )