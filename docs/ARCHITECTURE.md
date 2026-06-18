# Architecture

This project is a Python API test automation framework for the User Management API challenge. The scope is intentionally focused on REST API testing because the application under test is a service exposed through the OpenAPI contract in `sdet_challenge_api.yml`.

## Design Goals

1. Keep the automated tests aligned with the OpenAPI specification.
2. Cover all documented endpoints in both `dev` and `prod`.
3. Separate HTTP client logic from test intent.
4. Keep test data generation reusable and isolated.
5. Make known product bugs visible without hiding unexpected regressions.
6. Support local execution and GitHub Actions execution with the same commands and configuration model.
7. Keep framework unit tests separate from the E2E API suite.

## Project Structure

```text
api/                HTTP client layer
config/             Runtime settings and environment selection
models/             Pydantic models that mirror OpenAPI schemas
factories/          Test data builders
fixtures/           Pytest fixtures for clients, data, and cleanup
validators/         Reusable assertions and schema validators
tests/api/          Endpoint behavior tests
tests/contract/     Contract-focused error response tests
tests/unit/         Framework unit tests
docs/               Architecture, execution, matrices, and bug documentation
reports/            Generated HTML and JUnit XML reports
```

## Runtime Configuration

Runtime settings are centralized in `config/settings.py`.

The framework reads:

- `BASE_URL`
- `TEST_ENV`
- `AUTH_TOKEN`
- `REQUEST_TIMEOUT`
- `REQUEST_RETRIES`

`TEST_ENV` is validated against the only environments documented by the API spec:

- `dev`
- `prod`

This allows the same test code to run against either environment without branching inside test bodies.

## Client Layer

### `BaseClient`

`api/base_client.py` owns generic HTTP behavior:

- stores the configured environment
- builds URLs with the environment prefix
- exposes `get`, `post`, `put`, and `delete`
- delegates requests through `requests.Session`
- retries transient `GET` failures on `502`, `503`, and `504`

Example URL construction:

```text
BASE_URL=http://localhost:3000
TEST_ENV=dev
path=users

=> http://localhost:3000/dev/users
```

### `UsersClient`

`api/users_client.py` is the resource-specific client for `/users`.

It exposes readable domain operations:

- `list_users`
- `create_user`
- `create_user_raw`
- `get_user`
- `update_user`
- `update_user_role`
- `update_user_raw`
- `delete_user`

The typed methods use Pydantic request models. The `*_raw` methods intentionally bypass typed models so negative tests can send malformed-but-valid JSON payloads, such as missing required fields.

`UsersClient` also tracks successfully created or updated user emails so the cleanup fixture can delete test-created data after each test.

## Models And OpenAPI Alignment

The OpenAPI schemas are represented directly in `models/user.py`:

- `User`
- `CreateUserRequest`
- `UpdateUserRequest`
- `ErrorResponse`

The user payload models enforce:

- `name` as string
- `email` as valid email format
- `age` as integer between `1` and `150`

This keeps schema validation explicit and tied to the authoritative specification.

## Test Data Strategy

`factories/user_factory.py` creates valid and invalid test data.

The factory provides:

- valid create payloads
- valid update payloads
- missing-field payloads
- invalid-email payloads
- invalid-age payloads
- optional overrides through `UserOverrides`

Generated emails include a unique suffix to reduce collisions across repeated test runs. This matters because the challenge API can preserve data between runs.

## Fixtures And Cleanup

Fixtures are split by responsibility:

- `fixtures/api_fixtures.py`: API clients, environment settings, secondary environment client, cleanup
- `fixtures/data_fixtures.py`: reusable payload fixtures

The primary client uses the configured `TEST_ENV`.

The secondary client uses the opposite environment:

```text
TEST_ENV=dev  -> secondary=prod
TEST_ENV=prod -> secondary=dev
```

This supports the environment isolation test without duplicating test logic.

An autouse cleanup fixture runs after each test and deletes tracked users from both the primary and secondary clients. This keeps the E2E suite more repeatable and prevents stale test data from being mistaken for product bugs.

## Test Suite Layout

### API Tests

`tests/api/` contains endpoint behavior tests for:

- `GET /users`
- `POST /users`
- `GET /users/{email}`
- `PUT /users/{email}`
- `DELETE /users/{email}`
- environment isolation between `dev` and `prod`

These tests cover happy paths, validation failures, conflict handling, not-found behavior, authorization checks, and environment separation.

### Contract Tests

`tests/contract/` focuses on documented error responses.

These tests verify that known error paths return:

- documented status codes
- JSON content type
- `ErrorResponse` shape

This layer keeps error-contract validation explicit instead of scattering that concern only across endpoint tests.

### Unit Tests

`tests/unit/` validates the test framework itself.

These tests cover:

- settings parsing
- URL construction
- client request delegation
- user cleanup tracking
- factory behavior
- reusable validators

Unit tests are intentionally excluded from `make test-dev`, `make test-prod`, and the GitHub Actions E2E jobs. They can be run separately with:

```bash
make test-unit
```

## Markers And Traceability

Markers are declared in `pytest.ini`.

The main markers are:

- `api`
- `contract`
- `unit`
- `regression`
- `smoke`
- `security`
- `isolation`
- `tc_id`

`tc_id` markers map automated tests back to `docs/test_matrix.md`. This provides traceability between the OpenAPI requirements, the documented matrix, and the executable tests.

`docs/e2e_basic_matrix.md` serves a different purpose: it summarizes the smallest set of workflow-style E2E scenarios that are especially good at surfacing real product bugs such as failed persistence after successful writes.

## Known Bugs And `xfail`

Some tests expose confirmed mismatches between the implementation and `sdet_challenge_api.yml`.

Those tests are marked with `xfail` and reference `docs/bug_report.md`.

The goal is to:

- keep known product defects visible
- prevent known defects from hiding new regressions
- document why the failure is expected today

Only confirmed product mismatches are marked as `xfail`. Framework problems or test data issues are fixed in the framework rather than marked as expected failures.

## Reliability Strategy

The framework uses conservative network-level retries in `BaseClient`.

Retries apply only to `GET` requests and only for transient infrastructure-style responses:

- `502`
- `503`
- `504`

Mutating operations such as `POST`, `PUT`, and `DELETE` are not retried automatically. This avoids accidentally hiding product behavior or repeating state-changing requests.

Full pytest test reruns are intentionally not enabled by default. A rerun plugin can be useful in some large suites, but for this challenge it could mask real contract bugs, so known product defects are handled with explicit `xfail` instead.

## Parallel Execution Strategy

The suite is intentionally configured for sequential execution today.

That is the right tradeoff for the current size of the project because:

- the suite is still small enough that worker startup cost may outweigh the gain
- sequential execution is easier to debug during local reproduction and live interview discussion
- the main reliability risks so far have come from shared application state, not raw test runtime

The framework is already structured in a way that makes future parallelization realistic:

- generated emails are unique
- tests clean up their own created data
- unit tests are separated from E2E tests
- `dev` and `prod` already run in parallel at the workflow-job level

When the suite grows enough that parallel pytest workers become worthwhile, the scaling plan is:

1. Add `pytest-xdist` back to `requirements.txt`.
2. Add a worker control variable such as `PYTEST_WORKERS` to `.env.example`.
3. Update the Makefile to pass `-n <workers> --dist=loadscope` to pytest when that variable is set.
4. Set the worker count explicitly in `.github/workflows/tests.yml` after validating the suite remains stable in CI.
5. Benchmark sequential vs parallel execution before keeping the change permanently.

Until that point, sequential execution keeps the framework simpler and failures easier to interpret.

## Local Execution

The Makefile provides the main local workflow:

```bash
make setup
make up
make test-dev
make test-prod
make test-unit
make down
```

`test-dev` and `test-prod` run the E2E API and contract tests only:

```bash
pytest -m "not unit"
```

`test-unit` runs only the framework unit tests:

```bash
pytest -m unit
```

## CI/CD Execution

GitHub Actions is configured in `.github/workflows/tests.yml`.

The pipeline has two independent jobs:

- `e2e-dev`
- `e2e-prod`

Each job:

1. checks out the repository
2. installs Python dependencies
3. starts the challenge API container
4. waits for the target environment endpoint to respond
5. runs `pytest -m "not unit"`
6. writes a GitHub Actions job summary from the generated JUnit XML
7. uploads HTML and JUnit XML reports as artifacts

The jobs are separate so `dev` and `prod` run in parallel and one environment does not block the other.

`AUTH_TOKEN` is sourced from the repository secret `AUTH_TOKEN` when available. The workflow falls back to `mysecrettoken` only because the interview challenge container uses that static value by default.

## Reports

The framework generates:

- HTML reports for human-readable debugging
- JUnit XML reports for CI/CD integration
- GitHub Actions job summaries for quick review in the workflow UI

Examples:

```text
reports/dev-report.html
reports/dev-results.xml
reports/prod-report.html
reports/prod-results.xml
```

The GitHub summary is generated by `scripts/write_junit_summary.py`. That script reads a pytest JUnit XML file and publishes:

- totals for passed, failed, errored, `xfail`, and skipped tests
- short lists of failed cases
- short lists of `xfail` cases
- short lists of skipped cases

## Why This Design

This architecture keeps the test intent readable while still giving the framework enough structure to scale.

The most important design choices are:

- test code reads in business terms through `UsersClient`
- schema expectations live in Pydantic models
- reusable payloads come from factories
- fixtures own setup and cleanup
- validators keep assertions consistent
- contract tests make spec mismatches explicit
- unit tests protect the framework utilities
- CI runs `dev` and `prod` independently as required by the challenge
