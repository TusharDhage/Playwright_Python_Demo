# Playwright Python Demo Framework

[![Playwright Tests](https://github.com/TusharDhage/Playwright_Python_Demo/actions/workflows/playwright-ci.yml/badge.svg)](https://github.com/TusharDhage/Playwright_Python_Demo/actions/workflows/playwright-ci.yml)
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Playwright](https://img.shields.io/badge/Playwright-latest-green?logo=playwright)
![pytest](https://img.shields.io/badge/pytest-latest-orange)
![CI](https://img.shields.io/badge/CI-GitHub%20Actions-black?logo=githubactions)
![WireMock](https://img.shields.io/badge/WireMock-service--mocking-orange)
![LambdaTest](https://img.shields.io/badge/LambdaTest-cross--browser-blueviolet)
![Bandit](https://img.shields.io/badge/SAST-Bandit-red)

A production-ready test automation framework built with **Playwright** and **Python**, covering UI automation, API automation, service mocking (WireMock), cross-browser testing (LambdaTest), and security scanning (Bandit SAST).

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.11 | Core language |
| Playwright | Browser UI + API automation (`APIRequestContext`) |
| pytest | Test runner |
| pytest-html | HTML test reports |
| Allure | Rich test reports with screenshots |
| GitHub Actions | CI/CD pipeline |
| WireMock | Mocking external/internal service dependencies |
| LambdaTest | Cross-browser / cross-platform cloud testing |
| Postman | Manual, exploratory, and contract API validation |
| Bandit | SAST (Static Application Security Testing) |
| Page Object Model | Framework design pattern |

---

## Framework Structure

```
Playwright_Python_Demo/
├── .github/
│   └── workflows/
│       └── playwright-ci.yml       # CI: API + WireMock + LambdaTest + SAST jobs
├── pages/                          # Page Object classes (UI tests)
├── tests/
│   ├── api/
│   │   ├── conftest.py             # APIRequestContext fixture (session-scoped)
│   │   └── test_posts_api.py       # Playwright API tests (GET/POST/PUT/PATCH/DELETE)
│   ├── wiremock/
│   │   └── test_wiremock_services.py  # Tests against mocked services
│   └── test_*.py                   # UI tests (existing)
├── wiremock/
│   ├── docker-compose.yml          # Starts WireMock server locally
│   └── mappings/
│       ├── get_user.json           # Stub: GET /api/users/1
│       ├── create_user.json        # Stub: POST /api/users
│       ├── payment_service.json    # Stub: POST /api/payment/process
│       └── external_service_failure.json  # Stub: 503 failure simulation
├── postman/
│   └── Playwright_Demo_API_Collection.postman_collection.json
├── utils/
│   └── lambdatest_config.py        # LambdaTest CDP URL + capabilities builder
├── reports/                        # HTML test reports (git-ignored)
├── allure-results/                 # Allure raw results (git-ignored)
├── conftest.py                     # Root fixtures: browser, API, WireMock, LambdaTest, screenshots
├── pytest.ini                      # Markers, test paths, addopts
└── requirements.txt                # All dependencies
```

---

## Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/TusharDhage/Playwright_Python_Demo.git
cd Playwright_Python_Demo
pip install -r requirements.txt
playwright install
```

---

## Running Tests

### Run All API Tests
```bash
pytest tests/api/ -v -m api
```
Uses Playwright's native `APIRequestContext` — no browser launched, pure HTTP calls with full schema assertions.

### Run WireMock Tests (requires Docker)
```bash
# Step 1: Start WireMock server with all stub mappings
cd wiremock && docker-compose up -d

# Step 2: Load stubs (first time or after restart)
for f in mappings/*.json; do
  curl -X POST http://localhost:8080/__admin/mappings \
    -H "Content-Type: application/json" -d @"$f"
done

# Step 3: Run tests
cd ..
pytest tests/wiremock/ -v -m wiremock
```

### Run UI Tests (local)
```bash
pytest tests/ -v -m smoke
pytest tests/ -v -m regression
```

### Run on LambdaTest (cross-browser)
```bash
export LT_USERNAME=your_username
export LT_ACCESS_KEY=your_access_key
export LT_BROWSER=chrome   # or firefox, safari, edge

pytest tests/ -m smoke
```

### Run SAST scan
```bash
bandit -r . --exclude ./.venv,./__pycache__ -f json -o reports/bandit-report.json
```

### Run Specific Marker
```bash
pytest -m "api and smoke"       # API smoke tests only
pytest -m "regression and not wiremock"   # Regression, skip WireMock
```

---

## Priority 1: Playwright API Automation

**Files:** `tests/api/conftest.py`, `tests/api/test_posts_api.py`

Uses Playwright's built-in `APIRequestContext` — this is the "Playwright API" Cognizant refers to. It's faster than UI tests and integrates natively with Playwright's reporting and tracing.

```python
def test_get_post_by_id(self, api_request_context):
    response = api_request_context.get("/posts/1")
    assert response.status == 200
    body = response.json()
    assert body["id"] == 1
```

**Covers:**
- GET single and list resources
- POST / PUT / PATCH / DELETE
- Schema validation (field presence checks)
- Query parameter filtering
- 404 / negative scenario handling
- Response header (`Content-Type`) validation

---

## Priority 2: WireMock Service Mocking

**Files:** `wiremock/`, `tests/wiremock/test_wiremock_services.py`

WireMock simulates external service dependencies so tests are **fast, reliable, and isolated** — no real network calls needed.

**What's mocked:**

| Stub | Method | URL | Response |
|---|---|---|---|
| Get User | GET | `/api/users/1` | 200 + user JSON |
| Create User | POST | `/api/users` | 201 + created user |
| Payment Service | POST | `/api/payment/process` | 200 + SUCCESS |
| Inventory (failure) | GET | `/api/external/inventory` | 503 Service Unavailable |

The failure stub simulates downstream service outages — lets you test your app's **error handling** without breaking the real service.

---

## Priority 3: LambdaTest Cross-Browser Testing

**Files:** `utils/lambdatest_config.py`, `.github/workflows/playwright-ci.yml`

Tests tagged `@pytest.mark.smoke` run on **Chrome and Firefox** in parallel on LambdaTest grid in CI (on push to `main` branch).

**GitHub Secrets needed:**
```
LT_USERNAME      → Your LambdaTest username
LT_ACCESS_KEY    → Your LambdaTest access key
```
Get these free at [lambdatest.com](https://lambdatest.com).

---

## Priority 4: Postman Collection

**File:** `postman/Playwright_Demo_API_Collection.postman_collection.json`

Import into Postman for:
- **Exploratory testing** — manual API calls during dev/debug
- **Contract validation** — Postman test scripts verify schema
- **WireMock validation** — separate environment pointing to `localhost:8080`

**Import steps:**
1. Open Postman → Import → Upload `postman/Playwright_Demo_API_Collection.postman_collection.json`
2. Set `base_url` variable to `https://jsonplaceholder.typicode.com`
3. Set `wiremock_url` to `http://localhost:8080` (after starting WireMock)

---

## Priority 5: Bandit SAST

Bandit runs automatically in CI on every push. It scans all Python files for common security issues (hardcoded passwords, use of `eval`, SQL injection patterns, etc.).

```bash
bandit -r . --severity-level medium
```

---

## CI/CD Pipeline (GitHub Actions)

The updated `playwright-ci.yml` runs **5 parallel jobs**:

```
┌──────────────────────┐  ┌────────────────────────┐
│  Job 1: API Tests    │  │  Job 2: WireMock Tests  │
│  (Playwright)        │  │  (Docker service)       │
└──────────┬───────────┘  └───────────┬─────────────┘
           │                          │
           └──────────┬───────────────┘
                      ▼
           ┌─────────────────────┐
           │  Job 5: Allure      │
           │  Report (aggregated)│
           └─────────────────────┘

┌─────────────────────────┐  ┌────────────────────┐
│  Job 3: LambdaTest UI   │  │  Job 4: Bandit SAST │
│  chrome + firefox matrix│  │  Security Scan      │
└─────────────────────────┘  └────────────────────┘
```

---

## Markers Reference

| Marker | Description |
|---|---|
| `smoke` | Quick checks on every deploy |
| `regression` | Full suite before release |
| `api` | Playwright API tests |
| `wiremock` | Requires WireMock Docker container |
| `lambdatest` | Cross-browser on LambdaTest grid |
| `login` | Login flow tests |
| `navigation` | Navigation tests |

---

## Reporting

| Report | Location | When Generated |
|---|---|---|
| HTML Report | `reports/report.html` | Every run |
| Allure Report | `allure-results/` | Every run |
| LambdaTest Dashboard | lambdatest.com | CI (main branch) |
| Bandit SAST JSON | `reports/bandit-report.json` | CI every push |