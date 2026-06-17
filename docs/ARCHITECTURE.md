# Architecture

This framework is organized around API automation only, because the challenge scope is limited to a REST service.

## Design Goals

1. Keep the test suite aligned to the OpenAPI specification.
2. Separate reusable client logic from test intent.
3. Isolate domain models from test data factories.
4. Keep environment-specific execution simple for local runs and CI.

## OpenAPI Alignment

The framework models the schemas defined in `sdet_challenge_api.yml` directly in code:

- `User`
- `CreateUserRequest`
- `UpdateUserRequest`
- `ErrorResponse`

This keeps the tests tied to the authoritative API contract and makes schema validation explicit instead of implicit.
