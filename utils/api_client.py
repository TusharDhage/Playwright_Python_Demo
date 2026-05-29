import requests
import allure


class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def get(self, endpoint: str, params: dict = None):
        url = f"{self.base_url}{endpoint}"
        with allure.step(f"GET {url}"):
            response = self.session.get(url, params=params)
            self._log_response(response)
            return response

    def post(self, endpoint: str, payload: dict = None):
        url = f"{self.base_url}{endpoint}"
        with allure.step(f"POST {url}"):
            response = self.session.post(url, json=payload)
            self._log_response(response)
            return response

    def put(self, endpoint: str, payload: dict = None):
        url = f"{self.base_url}{endpoint}"
        with allure.step(f"PUT {url}"):
            response = self.session.put(url, json=payload)
            self._log_response(response)
            return response

    def delete(self, endpoint: str):
        url = f"{self.base_url}{endpoint}"
        with allure.step(f"DELETE {url}"):
            response = self.session.delete(url)
            self._log_response(response)
            return response

    def _log_response(self, response):
        print(f"\nStatus: {response.status_code}")
        print(f"Response: {response.text[:200]}")