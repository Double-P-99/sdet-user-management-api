# User Management API Test Framework

API E2E and contract test framework for the SDET take-home challenge.

## What This Project Covers

- E2E API tests for all documented user endpoints
- Contract-focused validation for documented error responses
- Environment-aware execution against `dev` and `prod`
- Local execution with Docker
- Parallel CI execution in GitHub Actions

## Structure

- `api/`: reusable API clients
- `config/`: environment and runtime settings
- `models/`: domain models
- `factories/`: test data builders
- `fixtures/`: pytest fixtures
- `validators/`: reusable API assertions
- `tests/api/`: endpoint behavior tests
- `tests/contract/`: contract and error response tests
- `docs/`: architecture, execution, and bug documentation
- `reports/`: generated test reports

## Configuration

The framework reads these environment variables:

- `BASE_URL`
- `TEST_ENV`
- `AUTH_TOKEN`
- `REQUEST_TIMEOUT`
- `REQUEST_RETRIES`

See [`.env.example`](./.env.example) for the default local values.

## Quick Start

### WSL or Git Bash

Use the Makefile flow if you are running in WSL, Git Bash, or another shell with `make` available:

```bash
make setup
make up
make test-dev
make test-prod
make down
```

### Windows PowerShell

If you are running from the Windows terminal without `make`, use the manual flow:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env -ErrorAction SilentlyContinue
docker run -d --name sdet-user-api -p 3000:3000 ghcr.io/danielsilva-loanpro/sdet-interview-challenge:latest
$env:TEST_ENV="dev"
.venv\Scripts\python.exe -m pytest --html=reports/dev-report.html --self-contained-html
$env:TEST_ENV="prod"
.venv\Scripts\python.exe -m pytest --html=reports/prod-report.html --self-contained-html
docker rm -f sdet-user-api
```

## Running the Test Suites

- `dev`: run against `http://localhost:3000/dev`
- `prod`: run against `http://localhost:3000/prod`
- `contract`: run the contract-focused error response checks

Examples:

```bash
make test-dev
make test-prod
make test-contract
```

```powershell
$env:TEST_ENV="dev"
.venv\Scripts\python.exe -m pytest

$env:TEST_ENV="prod"
.venv\Scripts\python.exe -m pytest

.venv\Scripts\python.exe -m pytest -m contract
```

## Reports

HTML reports are written to `reports/`:

- `reports/dev-report.html`
- `reports/prod-report.html`
- `reports/contract-report.html`
- `reports/report.html`

JUnit XML reports are also generated:

- `reports/dev-results.xml`
- `reports/prod-results.xml`
- `reports/contract-results.xml`
- `reports/results.xml`

Use the HTML files for detailed human-readable debugging. Use the JUnit XML files for CI/CD integrations and workflow-native summaries.

## Notes

- `make setup` creates `.venv`, installs dependencies there, and creates `.env` if needed.
- The Makefile is most convenient in WSL, Git Bash, or any Unix-like shell with `make`.
- PowerShell users can run the same workflow manually with `.venv\Scripts\python.exe`.
- Docker must be running before executing the tests locally.
- Additional execution details are documented in [RUNNING_TESTS.md](./docs/RUNNING_TESTS.md).
