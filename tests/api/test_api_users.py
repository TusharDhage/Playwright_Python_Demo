import pytest
import allure
from utils.api_client import APIClient

BASE_URL = "https://jsonplaceholder.typicode.com"


@pytest.fixture(scope="module")
def api():
    return APIClient(BASE_URL)


@allure.feature("Users API")
class TestUsersAPI:

    @allure.story("Get all users")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.api
    def test_get_all_users_returns_200(self, api):
        with allure.step("Send GET /users"):
            response = api.get("/users")
        with allure.step("Verify status code is 200"):
            assert response.status_code == 200
        with allure.step("Verify response is a list"):
            assert isinstance(response.json(), list)
        with allure.step("Verify 10 users returned"):
            assert len(response.json()) == 10

    @allure.story("Get single user")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.api
    def test_get_single_user_returns_correct_data(self, api):
        with allure.step("Send GET /users/1"):
            response = api.get("/users/1")
        with allure.step("Verify status code is 200"):
            assert response.status_code == 200
        with allure.step("Verify user data"):
            user = response.json()
            assert user["id"] == 1
            assert "name" in user
            assert "email" in user
            assert "username" in user

    @allure.story("Get single user")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.api
    def test_get_nonexistent_user_returns_404(self, api):
        with allure.step("Send GET /users/9999"):
            response = api.get("/users/9999")
        with allure.step("Verify status code is 404"):
            assert response.status_code == 404

    @allure.story("Create user")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.api
    def test_create_user_returns_201(self, api):
        payload = {
            "name": "Tushar Dhage",
            "username": "tushar",
            "email": "tushar@test.com"
        }
        with allure.step("Send POST /users with payload"):
            response = api.post("/users", payload)
        with allure.step("Verify status code is 201"):
            assert response.status_code == 201
        with allure.step("Verify created user data"):
            created = response.json()
            assert created["name"] == "Tushar Dhage"
            assert "id" in created

    @allure.story("Update user")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.api
    def test_update_user_returns_200(self, api):
        payload = {"name": "Tushar Updated"}
        with allure.step("Send PUT /users/1"):
            response = api.put("/users/1", payload)
        with allure.step("Verify status code is 200"):
            assert response.status_code == 200
        with allure.step("Verify updated name"):
            assert response.json()["name"] == "Tushar Updated"

    @allure.story("Delete user")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.api
    def test_delete_user_returns_200(self, api):
        with allure.step("Send DELETE /users/1"):
            response = api.delete("/users/1")
        with allure.step("Verify status code is 200"):
            assert response.status_code == 200

    @allure.story("Get all users")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    @pytest.mark.api
    @pytest.mark.parametrize("user_id", [1, 2, 3, 4, 5])
    def test_multiple_users_exist(self, api, user_id):
        with allure.step(f"Send GET /users/{user_id}"):
            response = api.get(f"/users/{user_id}")
        with allure.step("Verify user exists"):
            assert response.status_code == 200
            assert response.json()["id"] == user_id