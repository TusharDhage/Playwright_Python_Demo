import pytest
from playwright.sync_api import Page

def test_google_title(page: Page):
    page.goto("https://www.google.com")
    assert "Google" in page.title()

def test_playwright_website(page: Page):
    page.goto("https://playwright.dev")
    assert page.title() != ""