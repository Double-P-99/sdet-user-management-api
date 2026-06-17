# Bug Report

This report documents API behaviors observed on June 17, 2026 that do not match the contract defined in `sdet_challenge_api.yml`.

## Confirmed Bugs

| ID | Endpoint | Expected | Actual | Evidence |
| --- | --- | --- | --- | --- |
| BUG-001 | `POST /{env}/users` with invalid email | `400` with `ErrorResponse`, because `CreateUserRequest.email` is documented with `format: email` | `500 Internal Server Error` with `{ "error": "Internal server error" }` | Exposed by `tests/api/test_create_user.py` and reproduced manually with `POST /dev/users` using `{"name":"Bad Email","email":"invalid-email","age":30}` |
| BUG-002 | `DELETE /{env}/users/{email}` without `Authentication` header | `401` with `ErrorResponse`, because the header is required by the spec | `204 No Content`; the user is deleted successfully even with no auth header | Exposed by `tests/api/test_delete_user.py` and reproduced manually on June 17, 2026 with `DELETE /dev/users/delete.noheader.1781732589@example.com` |
| BUG-003 | `DELETE /{env}/users/{email}` with invalid `Authentication` header | `401` with `ErrorResponse` | `204 No Content`; the user is deleted successfully even with `Authentication: wrong-token` | Exposed by `tests/api/test_delete_user.py` and reproduced manually on June 17, 2026 with `DELETE /dev/users/delete.auth.1781732570@example.com` |
| BUG-004 | `GET /{env}/users` response schema | `200` with an array of `User` objects. Each `User.email` must match the schema’s `format: email` | The endpoint returns at least one persisted user with `email: "invalid-email"`, which violates the documented `User` schema | Observed manually on June 17, 2026 in `GET /dev/users`, which returned `{"age":30,"email":"invalid-email","name":"Test User 9"}` |

## Notes

- I intentionally excluded “extra field accepted” from this bug report because the OpenAPI schema does not explicitly forbid additional properties.
- The bugs above are direct mismatches against documented status codes, required auth behavior, or response schema definitions.
