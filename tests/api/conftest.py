import pytest


BASE_URL = "https://jsonplaceholder.typicode.com"


@pytest.fixture(scope="session")
def api_base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def api_request_context(playwright):
    """
    Playwright APIRequestContext — reused across all API tests in the session.
    Automatically disposes after the session ends.
    """
    context = playwright.request.new_context(
        base_url=BASE_URL,
        extra_http_headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    yield context
    context.dispose()