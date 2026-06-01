"""
Priority 1: Playwright API Automation
--------------------------------------
Uses Playwright's native APIRequestContext (NOT requests library).
Covers: GET, POST, PUT, PATCH, DELETE + schema validation + status checks.
Target: https://jsonplaceholder.typicode.com (public mock REST API)
"""

import pytest
import allure


@allure.feature("Posts API")
@allure.story("GET Requests")
class TestGetPosts:

    @allure.title("GET all posts returns 200 and non-empty list")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_all_posts(self, api_request_context):
        response = api_request_context.get("/posts")

        assert response.status == 200, f"Expected 200, got {response.status}"
        body = response.json()
        assert isinstance(body, list), "Response should be a list"
        assert len(body) == 100, f"Expected 100 posts, got {len(body)}"

    @allure.title("GET single post by ID returns correct post")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_post_by_id(self, api_request_context):
        response = api_request_context.get("/posts/1")

        assert response.status == 200
        body = response.json()
        # Schema validation
        assert "id" in body
        assert "title" in body
        assert "body" in body
        assert "userId" in body
        assert body["id"] == 1

    @allure.title("GET non-existent post returns 404")
    @pytest.mark.api
    @pytest.mark.regression
    def test_get_invalid_post_returns_404(self, api_request_context):
        response = api_request_context.get("/posts/9999")

        assert response.status == 404, f"Expected 404, got {response.status}"

    @allure.title("GET posts filtered by userId")
    @pytest.mark.api
    @pytest.mark.regression
    def test_get_posts_by_user(self, api_request_context):
        response = api_request_context.get("/posts", params={"userId": 1})

        assert response.status == 200
        body = response.json()
        assert len(body) > 0, "Should return posts for userId=1"
        for post in body:
            assert post["userId"] == 1, "All posts must belong to userId=1"


@allure.feature("Posts API")
@allure.story("POST / PUT / PATCH / DELETE")
class TestCrudPosts:

    @allure.title("POST creates a new post and returns 201")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_create_post(self, api_request_context):
        payload = {
            "title": "Automation Test Post",
            "body": "This post was created by Playwright API test",
            "userId": 1,
        }
        response = api_request_context.post("/posts", data=payload)

        assert response.status == 201, f"Expected 201, got {response.status}"
        body = response.json()
        assert body["title"] == payload["title"]
        assert body["body"] == payload["body"]
        assert "id" in body  # server assigns an id

    @allure.title("PUT replaces a post entirely and returns 200")
    @pytest.mark.api
    @pytest.mark.regression
    def test_update_post_put(self, api_request_context):
        payload = {
            "id": 1,
            "title": "Updated Title via PUT",
            "body": "Updated body content",
            "userId": 1,
        }
        response = api_request_context.put("/posts/1", data=payload)

        assert response.status == 200
        body = response.json()
        assert body["title"] == "Updated Title via PUT"

    @allure.title("PATCH updates partial fields of a post")
    @pytest.mark.api
    @pytest.mark.regression
    def test_update_post_patch(self, api_request_context):
        payload = {"title": "Patched Title"}
        response = api_request_context.patch("/posts/1", data=payload)

        assert response.status == 200
        body = response.json()
        assert body["title"] == "Patched Title"
        # Other fields should still exist (not wiped by PATCH)
        assert "body" in body

    @allure.title("DELETE a post returns 200")
    @pytest.mark.api
    @pytest.mark.regression
    def test_delete_post(self, api_request_context):
        response = api_request_context.delete("/posts/1")

        assert response.status == 200


@allure.feature("Comments API")
@allure.story("Nested resource validation")
class TestComments:

    @allure.title("GET comments for a post via query param")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_comments_for_post(self, api_request_context):
        response = api_request_context.get("/comments", params={"postId": 1})

        assert response.status == 200
        body = response.json()
        assert len(body) > 0
        for comment in body:
            assert comment["postId"] == 1
            assert "email" in comment

    @allure.title("GET comments via nested route /posts/1/comments")
    @pytest.mark.api
    @pytest.mark.regression
    def test_get_comments_nested_route(self, api_request_context):
        response = api_request_context.get("/posts/1/comments")

        assert response.status == 200
        body = response.json()
        assert isinstance(body, list)
        assert len(body) > 0


@allure.feature("Response Headers & Content-Type")
class TestResponseHeaders:

    @allure.title("Response Content-Type is application/json")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_response_content_type(self, api_request_context):
        response = api_request_context.get("/posts/1")

        content_type = response.headers.get("content-type", "")
        assert "application/json" in content_type, (
            f"Expected application/json, got: {content_type}"
        )