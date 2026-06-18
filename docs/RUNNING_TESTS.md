# Running Tests

## Prerequisites

1. Docker Desktop or Docker Engine is installed and running.
2. Python 3.11 or newer is available locally.
3. The repository has been cloned locally.
4. You are running either:
   `WSL` or another Unix-like shell with `make`, or `Windows PowerShell` with Python available.

## Environment Variables

The framework reads these variables:

- `BASE_URL`
- `TEST_ENV`
- `AUTH_TOKEN`
- `REQUEST_TIMEOUT`
- `REQUEST_RETRIES`

Default local values are documented in `.env.example`.

For local execution, the default `AUTH_TOKEN` is `mysecrettoken`.

For GitHub Actions, prefer configuring a repository secret named `AUTH_TOKEN`. The workflow falls back to `mysecrettoken` only when the secret is not set, which is acceptable for this challenge container but should not be treated as a general production pattern.

## WSL or Git Bash Workflow

This is the easiest path if `make` is available in your shell.

```bash
make setup
make up
make test-dev
make test-prod
make test-contract
make down
```

### What Each Command Does

```bash
make setup
```

Creates `.venv`, upgrades `pip`, installs `requirements.txt`, and creates `.env` from `.env.example` if `.env` does not already exist.

```bash
make up
```

Starts the challenge API container on `http://localhost:3000`.

```bash
make test-dev
make test-prod
make test-contract
```

Runs the corresponding test suites and writes HTML reports into `reports/`.

## Windows PowerShell Workflow

Use this path if you are working from Windows Terminal or PowerShell without `make`.

### 1. Create and populate the virtual environment

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 2. Create `.env` if needed

```powershell
Copy-Item .env.example .env -ErrorAction SilentlyContinue
```

### 3. Start the API container

```powershell
docker rm -f sdet-user-api
docker run -d --name sdet-user-api -p 3000:3000 ghcr.io/danielsilva-loanpro/sdet-interview-challenge:latest
```

### 4. Run tests against `dev`

```powershell
$env:TEST_ENV="dev"
.venv\Scripts\python.exe -m pytest --html=reports/dev-report.html --self-contained-html --junitxml=reports/dev-results.xml
```

### 5. Run tests against `prod`

```powershell
$env:TEST_ENV="prod"
.venv\Scripts\python.exe -m pytest --html=reports/prod-report.html --self-contained-html --junitxml=reports/prod-results.xml
```

### 6. Run contract-only tests

```powershell
$env:TEST_ENV="dev"
.venv\Scripts\python.exe -m pytest -m contract --html=reports/contract-report.html --self-contained-html --junitxml=reports/contract-results.xml
```

### 7. Stop the container

```powershell
docker rm -f sdet-user-api
```

## Manual Commands in WSL Without `make`

If you are in WSL but prefer not to use the Makefile, you can run the steps manually:

```bash
python -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
cp -n .env.example .env
docker rm -f sdet-user-api || true
docker run -d --name sdet-user-api -p 3000:3000 ghcr.io/danielsilva-loanpro/sdet-interview-challenge:latest
TEST_ENV=dev .venv/bin/python -m pytest --html=reports/dev-report.html --self-contained-html --junitxml=reports/dev-results.xml
TEST_ENV=prod .venv/bin/python -m pytest --html=reports/prod-report.html --self-contained-html --junitxml=reports/prod-results.xml
docker rm -f sdet-user-api
```

## Reports

Successful runs generate both HTML and JUnit XML artifacts in `reports/`, such as:

- `reports/dev-report.html`
- `reports/prod-report.html`
- `reports/contract-report.html`
- `reports/dev-results.xml`
- `reports/prod-results.xml`
- `reports/contract-results.xml`

In GitHub Actions, each environment job also writes a human-readable test summary into the workflow run using `scripts/write_junit_summary.py`.

## Report Types

### HTML Report

Generated automatically on each run, for example:

```bash
pytest --html=reports/report.html --self-contained-html
```

Open the file in a browser to inspect pass/fail status, traceback output, and the attached HTTP history for failed tests.

### JUnit XML

Generated alongside the HTML report, for example:

```bash
pytest --junitxml=reports/results.xml
```

JUnit XML is designed for CI/CD systems. GitHub Actions and other test tooling can parse it directly to display a native summary in the workflow UI without downloading an artifact.

### GitHub Actions Summary

The workflow reads the generated JUnit XML and writes a compact summary into the GitHub Actions job UI. The summary includes:

- passed count
- failed count
- error count
- `xfail` count
- skipped count
- short lists of failed, `xfail`, and skipped test cases

This gives reviewers a fast read on the run outcome without downloading the HTML artifact first.

## Troubleshooting

- If Docker is not running, the API container will fail to start.
- If port `3000` is already in use, stop the conflicting process or remap the port and update `BASE_URL`.
- If `make` is not recognized in Windows, use the PowerShell workflow instead of the Makefile.
- If dependencies are missing, rerun the virtual environment installation step before running tests.
- `REQUEST_RETRIES` controls conservative client-level retries for transient `GET` failures with HTTP `502`, `503`, or `504`. Full test reruns are intentionally not enabled by default because they can hide real API contract bugs.
