"""
Priority 2: WireMock Service Mocking Tests
-------------------------------------------
These tests run against a local WireMock server (port 8080).
WireMock simulates external/internal service dependencies so tests
are fast, reliable, and independent of real upstream services.

To run locally:
    cd wiremock && docker-compose up -d
    pytest tests/wiremock/ -v -m wiremock

In CI, WireMock is started automatically as a service container.
"""

import pytest
import requests
import allure

WIREMOCK_BASE = "http://localhost:8080"


@pytest.fixture(scope="module")
def wiremock_url():
    return WIREMOCK_BASE


def is_wiremock_running(base_url: str) -> bool:
    """Checks if WireMock server is reachable before running tests."""
    try:
        r = requests.get(f"{base_url}/__admin/mappings", timeout=3)
        return r.status_code == 200
    except Exception:
        return False


@pytest.fixture(autouse=True, scope="module")
def require_wiremock(wiremock_url):
    if not is_wiremock_running(wiremock_url):
        pytest.skip(
            "WireMock is not running. Start it with: cd wiremock && docker-compose up -d"
        )


@allure.feature("WireMock - User Service")
class TestMockedUserService:

    @allure.title("GET /api/users/1 returns mocked user data")
    @pytest.mark.wiremock
    @pytest.mark.smoke
    def test_get_mocked_user(self, wiremock_url):
        response = requests.get(f"{wiremock_url}/api/users/1")

        assert response.status_code == 200
        body = response.json()
        assert body["id"] == 1
        assert body["name"] == "Tushar Dhage"
        assert body["active"] is True

    @allure.title("POST /api/users creates mocked user and returns 201")
    @pytest.mark.wiremock
    @pytest.mark.smoke
    def test_create_mocked_user(self, wiremock_url):
        payload = {"name": "New User", "email": "newuser@example.com"}
        response = requests.post(
            f"{wiremock_url}/api/users",
            json=payload,
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code == 201
        body = response.json()
        assert "id" in body
        assert body["active"] is True


@allure.feature("WireMock - External Payment Service")
class TestMockedPaymentService:

    @allure.title("POST /api/payment/process returns mocked SUCCESS response")
    @pytest.mark.wiremock
    @pytest.mark.regression
    def test_payment_service_mocked_success(self, wiremock_url):
        payload = {"amount": 1500.00, "currency": "INR", "userId": 1}
        response = requests.post(f"{wiremock_url}/api/payment/process", json=payload)

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "SUCCESS"
        assert "transactionId" in body
        assert body["transactionId"].startswith("TXN-")


@allure.feature("WireMock - Failure Simulation")
class TestMockedServiceFailures:

    @allure.title("GET /api/external/inventory returns mocked 503 failure")
    @pytest.mark.wiremock
    @pytest.mark.regression
    def test_inventory_service_unavailable(self, wiremock_url):
        """
        Validates that our app handles downstream failures correctly.
        WireMock simulates the inventory service returning 503.
        """
        response = requests.get(f"{wiremock_url}/api/external/inventory")

        assert response.status_code == 503
        body = response.json()
        assert "error" in body
        assert body["error"] == "Service Unavailable"


@allure.feature("WireMock - Admin API")
class TestWireMockAdmin:

    @allure.title("WireMock admin endpoint lists all registered stubs")
    @pytest.mark.wiremock
    def test_admin_lists_all_stubs(self, wiremock_url):
        """Verifies all expected stub mappings are loaded in WireMock."""
        response = requests.get(f"{wiremock_url}/__admin/mappings")

        assert response.status_code == 200
        body = response.json()
        assert "mappings" in body
        # We have 4 stub mappings defined
        assert len(body["mappings"]) >= 4, (
            f"Expected at least 4 stub mappings, found {len(body['mappings'])}"
        )