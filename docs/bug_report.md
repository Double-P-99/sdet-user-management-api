# Bug Report

This document records the discrepancies found between the runtime behavior of the API and the contract defined in `sdet_challenge_api.yml`.

All bugs below were confirmed from the automated suite and corroborated with the generated reports on June 18, 2026.

## BUG-001: `POST /users` accepts invalid email format

**Summary**  
The API accepts a payload with an invalid email and creates the user successfully, even though the OpenAPI contract defines `email` with `format: email`.

**Specification expectation**
- Endpoint: `POST /{env}/users`
- Expected status: `400`
- Expected body: `ErrorResponse`
- Contract reference: `CreateUserRequest.email` uses `format: email`

**Actual behavior**
- The API returns `201 Created`
- The invalid user is persisted
- The response body echoes the invalid email value

**Affected environments**
- `dev`
- `prod`

**Test cases that exposed it**
- `TC-016`: invalid email format in `dev`
- `TC-017`: invalid email format in `prod`
- `TC-045`: error contract for create-user validation failure in `dev`
- `TC-046`: error contract for create-user validation failure in `prod`

**Automated evidence**
- `tests/api/test_create_user.py::test_create_user_returns_400_for_invalid_email`
- `tests/contract/test_error_responses.py::test_error_responses_follow_contract[create-user-validation-error]`
- Reflected in:
  - `reports/dev-results.xml`
  - `reports/prod-results.xml`

**Scenarios affected**
- Input validation for create-user requests
- Error-handling contract for validation failures
- Downstream collection integrity, because invalid records become visible in `GET /users`

## BUG-002: `POST /users` returns `500` instead of `409` for duplicate email

**Summary**  
Creating a user twice with the same email does not return the documented conflict response. Instead, the API fails with an internal server error.

**Specification expectation**
- Endpoint: `POST /{env}/users`
- Expected status: `409`
- Expected body: `ErrorResponse`

**Actual behavior**
- The first create request returns `201`
- The second create request with the same email returns `500 Internal Server Error`

**Affected environments**
- `dev`
- `prod`

**Test cases that exposed it**
- `TC-018`: duplicate email in `dev`
- `TC-019`: duplicate email in `prod`
- `TC-047`: error contract for duplicate email in `dev`
- `TC-048`: error contract for duplicate email in `prod`

**Automated evidence**
- `tests/api/test_create_user.py::test_create_user_returns_409_for_duplicate_email`
- `tests/contract/test_error_responses.py::test_error_responses_follow_contract[create-user-duplicate-email]`
- Reflected in:
  - `reports/dev-results.xml`
  - `reports/prod-results.xml`

**Scenarios affected**
- Conflict handling during user creation
- Error-response status code compliance
- Duplicate-data protection behavior

## BUG-003: `GET /users/{email}` returns `500` instead of `404` for missing user

**Summary**  
Fetching a user that does not exist should produce a not-found response, but the API returns an internal server error instead.

**Specification expectation**
- Endpoint: `GET /{env}/users/{email}`
- Expected status: `404`
- Expected body: `ErrorResponse`

**Actual behavior**
- The API returns `500 Internal Server Error`
- The response body is `{ "error": "Internal server error" }`

**Affected environments**
- `dev`
- `prod`

**Test cases that exposed it**
- `TC-022`: fetch nonexistent user in `dev`
- `TC-023`: fetch nonexistent user in `prod`
- `TC-049`: error contract for missing user in `dev`
- `TC-050`: error contract for missing user in `prod`

**Automated evidence**
- `tests/api/test_get_user.py::test_get_user_returns_404_for_unknown_user`
- `tests/contract/test_error_responses.py::test_error_responses_follow_contract[get-missing-user]`
- Reflected in:
  - `reports/dev-results.xml`
  - `reports/prod-results.xml`

**Scenarios affected**
- Not-found handling for direct user lookup
- Error contract for missing-resource scenarios
- Environment-isolation verification when the secondary environment should not know about the user

## BUG-004: `DELETE /dev/users/{email}` allows deletion without authentication

**Summary**  
The `dev` environment allows a delete request to succeed even when the required `Authentication` header is not provided.

**Specification expectation**
- Endpoint: `DELETE /{env}/users/{email}`
- Expected status: `401`
- Expected body: `ErrorResponse`
- Contract requirement: `Authentication` header is required

**Actual behavior**
- In `dev`, the API returns `204 No Content`
- The user is deleted successfully without authentication

**Affected environments**
- `dev` only

**Test cases that exposed it**
- `TC-037`: delete without auth header in `dev`
- `TC-055`: unauthorized delete error contract in `dev`

**Automated evidence**
- `tests/api/test_delete_user.py::test_delete_user_returns_401_without_auth_header`
- `tests/contract/test_error_responses.py::test_error_responses_follow_contract[delete-unauthorized]`
- Reflected in:
  - `reports/dev-results.xml`

**Environment comparison note**
- The equivalent `prod` scenario currently passes, so this bug is environment-specific based on the latest available evidence.

**Scenarios affected**
- Security and authorization enforcement
- Error-response contract for unauthorized deletion
- Consistency between `dev` and `prod`

## BUG-005: `DELETE /dev/users/{email}` accepts an invalid authentication token

**Summary**  
The `dev` environment does not validate the authentication token correctly for delete operations.

**Specification expectation**
- Endpoint: `DELETE /{env}/users/{email}`
- Expected status: `401`
- Expected body: `ErrorResponse`

**Actual behavior**
- In `dev`, the API returns `204 No Content`
- The delete succeeds even when `Authentication: wrong-token` is sent

**Affected environments**
- `dev` only

**Test cases that exposed it**
- `TC-039`: delete with invalid auth token in `dev`

**Automated evidence**
- `tests/api/test_delete_user.py::test_delete_user_returns_401_for_invalid_auth_token`
- Reflected in:
  - `reports/dev-results.xml`

**Environment comparison note**
- The equivalent `prod` scenario currently passes, so this behavior is not reproduced in `prod` in the latest run evidence.

**Scenarios affected**
- Security token validation
- Authorization consistency across environments
- Reliability of protected destructive operations

## BUG-006: `PUT /users/{email}` returns `200` but does not persist updates reliably

**Summary**  
The API reports successful user updates with `200 OK`, but the changes are not reliably persisted. This affects both primary-key updates (`email`) and non-key field updates (`name`, `age`).

**Specification expectation**
- Endpoint: `PUT /{env}/users/{email}`
- Expected status: `200`
- Expected behavior: subsequent reads should reflect the updated user state

**Actual behavior**
- The update request returns `200 OK`
- The update response body echoes the submitted values
- Follow-up reads do not consistently reflect the update:
  - When the `email` is changed, `GET /users/{new_email}` returns `500 Internal Server Error`
  - When the `email` stays the same, `GET /users` still returns the old `name` and `age`

**Affected environments**
- Confirmed in `dev`
- `prod` should be verified with the same scenarios

**Test cases that exposed it**
- Extended coverage under `TC-024`: successful update should persist for follow-up retrieval by updated email
- `TC-057`: unchanged-email update should persist in list results in `dev`
- `TC-058`: unchanged-email update should persist in list results in `prod`

**Automated evidence**
- `tests/api/test_update_user.py::test_update_user_persists_changes_for_followup_get`
- `tests/api/test_update_user.py::test_update_user_persists_field_changes_in_user_list_when_email_is_unchanged`
- Reflected in:
  - `reports/dev-results.xml`
  - `reports/dev-report.html`

**Scenarios affected**
- Resource persistence after update
- Primary-key change behavior when `email` is updated
- Read-after-write consistency for `PUT`
- Collection correctness after updating non-key user fields

## Notes

- The OpenAPI file was treated as the authoritative source for expected status codes, schemas, required authentication behavior, and environment usage.
- I intentionally did not report "extra fields accepted" as a bug because the schema does not explicitly define `additionalProperties: false`.
- During earlier runs, `GET /users` exposed invalid persisted records and looked like a separate response-schema bug. After adding unique test data and automatic cleanup, that behavior is no longer treated as a confirmed application bug and is considered historical test-environment contamination instead.
