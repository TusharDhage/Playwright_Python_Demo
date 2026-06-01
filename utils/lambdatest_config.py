"""
utils/lambdatest_config.py
---------------------------
LambdaTest cross-browser configuration for Playwright.

Setup:
    1. Create a free account at https://lambdatest.com
    2. Add your credentials as GitHub Secrets:
       - LT_USERNAME
       - LT_ACCESS_KEY
    3. Tests tagged @pytest.mark.smoke will run on LambdaTest grid in CI.

Local usage:
    export LT_USERNAME=your_username
    export LT_ACCESS_KEY=your_key
    pytest tests/ -m smoke --lt-browser=chrome
"""

import os


def get_lt_capabilities(browser: str = "chrome", build_name: str = "Playwright-Demo") -> dict:
    """
    Returns LambdaTest browser capabilities dict.
    Pass this to playwright.chromium.connect() for remote execution.
    """
    return {
        "browserName": browser,
        "browserVersion": "latest",
        "LT:Options": {
            "platform": "Windows 10",
            "build": build_name,
            "name": f"Playwright {browser} Test",
            "user": os.environ.get("LT_USERNAME", ""),
            "accessKey": os.environ.get("LT_ACCESS_KEY", ""),
            "network": True,
            "video": True,
            "console": True,
            "tunnel": False,
            "tunnelName": "",
        },
    }


def get_lt_cdp_url() -> str:
    """
    Returns the LambdaTest CDP WebSocket URL for Playwright.
    Usage in conftest.py:
        browser = playwright.chromium.connect(get_lt_cdp_url())
    """
    username = os.environ.get("LT_USERNAME", "")
    access_key = os.environ.get("LT_ACCESS_KEY", "")
    return f"wss://cdp.lambdatest.com/playwright?user={username}&accessKey={access_key}"


def is_lambdatest_enabled() -> bool:
    """Returns True if LambdaTest credentials are present in environment."""
    return bool(
        os.environ.get("LT_USERNAME") and os.environ.get("LT_ACCESS_KEY")
    )