# User Management API Test Framework

API E2E and contract test framework for the SDET take-home challenge.

## Overview

- E2E API tests for all documented user endpoints
- Contract-focused validation for documented error responses
- Environment-aware execution against `dev` and `prod`
- Local execution with Docker
- Parallel CI execution in GitHub Actions

This repository is intentionally structured to keep test intent readable while still making the framework maintainable:

- resource-specific client methods express API behavior in domain terms
- Pydantic models keep success and error schema validation explicit
- factories isolate test data creation
- fixtures handle setup and cleanup
- `xfail` keeps confirmed application bugs visible without hiding unrelated regressions

## Design Decisions

- `tests/api/`, `tests/contract/`, and `tests/unit/` are separated so endpoint behavior, contract validation, and framework verification stay distinct.
- `UsersClient` wraps HTTP details so tests read like workflows instead of request plumbing.
- `dev` and `prod` are executed as separate runs rather than branching inside test bodies.
- Cleanup is automatic after each test to reduce state contamination across runs.
- Retries are limited to `GET` requests for transient `502`, `503`, and `504` responses so mutating calls are not replayed accidentally.

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

## Documentation

- [Architecture](./docs/ARCHITECTURE.md)
- [Full Contract Test Matrix](./docs/test_matrix.md)
- [Basic E2E Matrix](./docs/e2e_basic_matrix.md)
- [Bug Report](./docs/bug_report.md)
- [Running Tests](./docs/RUNNING_TESTS.md)

## Configuration

The framework reads these environment variables:

- `BASE_URL`
- `TEST_ENV`
- `AUTH_TOKEN`
- `REQUEST_TIMEOUT`
- `REQUEST_RETRIES`

See [`.env.example`](./.env.example) for the default local values.

Local defaults are designed for the challenge container.
In GitHub Actions, `AUTH_TOKEN` is sourced from a repository secret when available.

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
docker rm -f sdet-user-api
docker run -d --name sdet-user-api -p 3000:3000 ghcr.io/danielsilva-loanpro/sdet-interview-challenge:latest
$env:TEST_ENV="dev"
.venv\Scripts\python.exe -m pytest -m "not unit" --html=reports/dev-report.html --self-contained-html --junitxml=reports/dev-results.xml
$env:TEST_ENV="prod"
.venv\Scripts\python.exe -m pytest -m "not unit" --html=reports/prod-report.html --self-contained-html --junitxml=reports/prod-results.xml
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
make test-unit
```

```powershell
$env:TEST_ENV="dev"
.venv\Scripts\python.exe -m pytest -m "not unit" --html=reports/dev-report.html --self-contained-html --junitxml=reports/dev-results.xml

$env:TEST_ENV="prod"
.venv\Scripts\python.exe -m pytest -m "not unit" --html=reports/prod-report.html --self-contained-html --junitxml=reports/prod-results.xml

$env:TEST_ENV="dev"
.venv\Scripts\python.exe -m pytest -m contract --html=reports/contract-report.html --self-contained-html --junitxml=reports/contract-results.xml

$env:TEST_ENV="dev"
.venv\Scripts\python.exe -m pytest -m unit
```

## CI/CD

GitHub Actions runs the suite in two independent jobs:

- `e2e-dev`
- `e2e-prod`

Each job:

1. starts the challenge API container
2. waits for the target environment to respond
3. runs `pytest -m "not unit"`
4. uploads HTML and JUnit XML reports
5. publishes a GitHub Actions job summary generated from the JUnit XML

This gives both environment separation and a fast CI feedback loop.

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

In GitHub Actions, the JUnit XML is also summarized directly in the job UI, including:

- passed count
- failed count
- error count
- `xfail` count
- skipped count

## Known Gaps With More Time

- malformed JSON body coverage for `POST /users` and `PUT /users/{email}`
- path-encoding edge cases for special email values
- exploratory invalid-email path cases for `GET`, `PUT`, and `DELETE`
- repeated-delete behavior after a successful `204`
- stronger bidirectional isolation checks
- stricter response schema drift checks
- more auth-header robustness coverage

## Notes

- `make setup` creates `.venv`, installs dependencies there, and creates `.env` if needed.
- The Makefile is most convenient in WSL, Git Bash, or any Unix-like shell with `make`.
- PowerShell users can run the same workflow manually with `.venv\Scripts\python.exe`.
- Docker must be running before executing the tests locally.
- Additional execution details are documented in [Running Tests](./docs/RUNNING_TESTS.md).
- The project includes both a full contract traceability matrix and a smaller workflow-focused E2E matrix so specification coverage and real user flows stay visible separately.
