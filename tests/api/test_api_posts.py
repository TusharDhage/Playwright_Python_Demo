import pytest
import allure
from utils.api_client import APIClient

BASE_URL = "https://jsonplaceholder.typicode.com"


@pytest.fixture(scope="module")
def api():
    return APIClient(BASE_URL)


@allure.feature("Posts API")
class TestPostsAPI:

    @allure.story("Get all posts")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.api
    def test_get_all_posts_returns_200(self, api):
        response = api.get("/posts")
        assert response.status_code == 200
        assert len(response.json()) == 100

    @allure.story("Create post")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.api
    def test_create_post(self, api):
        payload = {
            "title": "Playwright API Test",
            "body": "Testing API with requests library",
            "userId": 1
        }
        response = api.post("/posts", payload)
        assert response.status_code == 201
        assert response.json()["title"] == "Playwright API Test"

    @allure.story("Response time")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    @pytest.mark.api
    def test_response_time_under_2_seconds(self, api):
        response = api.get("/posts")
        assert response.elapsed.total_seconds() < 2, \
            f"Response too slow: {response.elapsed.total_seconds()}s"