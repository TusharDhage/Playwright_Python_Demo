import os

class Config:
    # Reads from environment variables (set by GitHub Secrets in CI)
    # Falls back to defaults for local development
    USERNAME = os.getenv("TEST_USERNAME", "student")
    PASSWORD = os.getenv("TEST_PASSWORD", "Password123")
    BASE_URL  = os.getenv(
        "BASE_URL",
        "https://practicetestautomation.com/practice-test-login/"
    )