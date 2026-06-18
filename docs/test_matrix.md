# Test Case Matrix

This matrix maps the OpenAPI specification to the automated scenarios implemented in the framework. It is intentionally more granular than the file-level coverage view so that each validation, auth, conflict, not-found, and environment-specific behavior is visible as an independent test case.

| TC ID | Endpoint | Method | Scenario | Environment | Priority | Expected Result | Automated Coverage |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TC-001 | `/users` | `GET` | List users in `dev` | `dev` | High | `200` with JSON array | `test_list_users_returns_200_and_json_array` |
| TC-002 | `/users` | `GET` | List users in `prod` | `prod` | High | `200` with JSON array | `test_list_users_returns_200_and_json_array` |
| TC-003 | `/users` | `GET` | Created user appears in list in `dev` | `dev` | High | `200`; created email is present in response | `test_list_users_includes_created_user` |
| TC-004 | `/users` | `GET` | Created user appears in list in `prod` | `prod` | High | `200`; created email is present in response | `test_list_users_includes_created_user` |
| TC-005 | `/users` | `GET` | Every item in list matches `User` schema in `dev` | `dev` | High | All collection elements validate as `User` | `test_list_users_includes_created_user` |
| TC-006 | `/users` | `GET` | Every item in list matches `User` schema in `prod` | `prod` | High | All collection elements validate as `User` | `test_list_users_includes_created_user` |
| TC-007 | `/users` | `POST` | Create user with valid payload in `dev` | `dev` | High | `201` with `User` response | `test_create_user_returns_201_and_created_user` |
| TC-008 | `/users` | `POST` | Create user with valid payload in `prod` | `prod` | High | `201` with `User` response | `test_create_user_returns_201_and_created_user` |
| TC-009 | `/users` | `POST` | Missing `name` in request body | `dev`, `prod` | High | `400` with `ErrorResponse` | `test_create_user_returns_400_for_missing_required_fields[name]` |
| TC-010 | `/users` | `POST` | Missing `email` in request body | `dev`, `prod` | High | `400` with `ErrorResponse` | `test_create_user_returns_400_for_missing_required_fields[email]` |
| TC-011 | `/users` | `POST` | Missing `age` in request body | `dev`, `prod` | High | `400` with `ErrorResponse` | `test_create_user_returns_400_for_missing_required_fields[age]` |
| TC-012 | `/users` | `POST` | Age equal to `0` | `dev`, `prod` | High | `400` with `ErrorResponse` | `test_create_user_returns_400_for_invalid_age[0]` |
| TC-013 | `/users` | `POST` | Age below minimum (`-1`) | `dev`, `prod` | Medium | `400` with `ErrorResponse` | `test_create_user_returns_400_for_invalid_age[-1]` |
| TC-014 | `/users` | `POST` | Age above maximum (`151`) | `dev`, `prod` | High | `400` with `ErrorResponse` | `test_create_user_returns_400_for_invalid_age[151]` |
| TC-015 | `/users` | `POST` | Age with invalid type (`\"thirty\"`) | `dev`, `prod` | Medium | `400` with `ErrorResponse` | `test_create_user_returns_400_for_invalid_age[thirty]` |
| TC-016 | `/users` | `POST` | Invalid email format in `dev` | `dev` | High | `400` with `ErrorResponse` | `test_create_user_returns_400_for_invalid_email` |
| TC-017 | `/users` | `POST` | Invalid email format in `prod` | `prod` | High | `400` with `ErrorResponse` | `test_create_user_returns_400_for_invalid_email` |
| TC-018 | `/users` | `POST` | Duplicate email in `dev` | `dev` | High | `409` with `ErrorResponse` | `test_create_user_returns_409_for_duplicate_email` |
| TC-019 | `/users` | `POST` | Duplicate email in `prod` | `prod` | High | `409` with `ErrorResponse` | `test_create_user_returns_409_for_duplicate_email` |
| TC-020 | `/users/{email}` | `GET` | Fetch existing user in `dev` | `dev` | High | `200` with `User` response | `test_get_user_returns_200_for_existing_user` |
| TC-021 | `/users/{email}` | `GET` | Fetch existing user in `prod` | `prod` | High | `200` with `User` response | `test_get_user_returns_200_for_existing_user` |
| TC-022 | `/users/{email}` | `GET` | Fetch nonexistent user in `dev` | `dev` | High | `404` with `ErrorResponse` | `test_get_user_returns_404_for_unknown_user` |
| TC-023 | `/users/{email}` | `GET` | Fetch nonexistent user in `prod` | `prod` | High | `404` with `ErrorResponse` | `test_get_user_returns_404_for_unknown_user` |
| TC-024 | `/users/{email}` | `PUT` | Update existing user in `dev` | `dev` | High | `200` with updated `User` response | `test_update_user_returns_200_and_updated_user` |
| TC-025 | `/users/{email}` | `PUT` | Update existing user in `prod` | `prod` | High | `200` with updated `User` response | `test_update_user_returns_200_and_updated_user` |
| TC-057 | `/users/{email}` -> `/users` | `PUT` -> `GET` | Update user without changing email and verify changed fields appear in list in `dev` | `dev` | High | `200`; listed user reflects updated `name` and `age` | `test_update_user_persists_field_changes_in_user_list_when_email_is_unchanged` |
| TC-058 | `/users/{email}` -> `/users` | `PUT` -> `GET` | Update user without changing email and verify changed fields appear in list in `prod` | `prod` | High | `200`; listed user reflects updated `name` and `age` | `test_update_user_persists_field_changes_in_user_list_when_email_is_unchanged` |
| TC-026 | `/users/{email}` | `PUT` | Missing `name` during update | `dev`, `prod` | High | `400` with `ErrorResponse` | `test_update_user_returns_400_for_missing_required_fields[name]` |
| TC-027 | `/users/{email}` | `PUT` | Missing `email` during update | `dev`, `prod` | High | `400` with `ErrorResponse` | `test_update_user_returns_400_for_missing_required_fields[email]` |
| TC-028 | `/users/{email}` | `PUT` | Missing `age` during update | `dev`, `prod` | High | `400` with `ErrorResponse` | `test_update_user_returns_400_for_missing_required_fields[age]` |
| TC-029 | `/users/{email}` | `PUT` | Invalid email format during update in `dev` | `dev` | High | `400` with `ErrorResponse` | `test_update_user_returns_400_for_invalid_email` |
| TC-030 | `/users/{email}` | `PUT` | Invalid email format during update in `prod` | `prod` | High | `400` with `ErrorResponse` | `test_update_user_returns_400_for_invalid_email` |
| TC-031 | `/users/{email}` | `PUT` | Update nonexistent user in `dev` | `dev` | High | `404` with `ErrorResponse` | `test_update_user_returns_404_for_unknown_user` |
| TC-032 | `/users/{email}` | `PUT` | Update nonexistent user in `prod` | `prod` | High | `404` with `ErrorResponse` | `test_update_user_returns_404_for_unknown_user` |
| TC-033 | `/users/{email}` | `PUT` | Update user to duplicate email in `dev` | `dev` | High | `409` with `ErrorResponse` | `test_update_user_returns_409_for_duplicate_email` |
| TC-034 | `/users/{email}` | `PUT` | Update user to duplicate email in `prod` | `prod` | High | `409` with `ErrorResponse` | `test_update_user_returns_409_for_duplicate_email` |
| TC-035 | `/users/{email}` | `DELETE` | Delete existing user with valid auth in `dev` | `dev` | High | `204` with empty response body | `test_delete_user_returns_204_for_existing_user` |
| TC-036 | `/users/{email}` | `DELETE` | Delete existing user with valid auth in `prod` | `prod` | High | `204` with empty response body | `test_delete_user_returns_204_for_existing_user` |
| TC-037 | `/users/{email}` | `DELETE` | Delete without auth header in `dev` | `dev` | High | `401` with `ErrorResponse` | `test_delete_user_returns_401_without_auth_header` |
| TC-038 | `/users/{email}` | `DELETE` | Delete without auth header in `prod` | `prod` | High | `401` with `ErrorResponse` | `test_delete_user_returns_401_without_auth_header` |
| TC-039 | `/users/{email}` | `DELETE` | Delete with invalid auth token in `dev` | `dev` | High | `401` with `ErrorResponse` | `test_delete_user_returns_401_for_invalid_auth_token` |
| TC-040 | `/users/{email}` | `DELETE` | Delete with invalid auth token in `prod` | `prod` | High | `401` with `ErrorResponse` | `test_delete_user_returns_401_for_invalid_auth_token` |
| TC-041 | `/users/{email}` | `DELETE` | Delete nonexistent user in `dev` | `dev` | Medium | `404` with `ErrorResponse` | `test_delete_user_returns_404_for_unknown_user` |
| TC-042 | `/users/{email}` | `DELETE` | Delete nonexistent user in `prod` | `prod` | Medium | `404` with `ErrorResponse` | `test_delete_user_returns_404_for_unknown_user` |
| TC-043 | `/dev` and `/prod` | Cross-environment | User created in `dev` should not exist in `prod` | Cross-environment | High | Secondary environment returns `404` | `test_users_are_isolated_between_environments` |
| TC-044 | `/dev` and `/prod` | Cross-environment | User created in `prod` should not exist in `dev` | Cross-environment | High | Secondary environment returns `404` | `test_users_are_isolated_between_environments` |
| TC-045 | Error contract | `POST /users` | Error schema for validation failures in `dev` | `dev` | High | `400` with `{ "error": "..." }` | `test_error_responses_follow_contract[create-user-validation-error]` |
| TC-046 | Error contract | `POST /users` | Error schema for validation failures in `prod` | `prod` | High | `400` with `{ "error": "..." }` | `test_error_responses_follow_contract[create-user-validation-error]` |
| TC-047 | Error contract | `POST /users` | Error schema for duplicate email in `dev` | `dev` | High | `409` with `{ "error": "..." }` | `test_error_responses_follow_contract[create-user-duplicate-email]` |
| TC-048 | Error contract | `POST /users` | Error schema for duplicate email in `prod` | `prod` | High | `409` with `{ "error": "..." }` | `test_error_responses_follow_contract[create-user-duplicate-email]` |
| TC-049 | Error contract | `GET /users/{email}` | Error schema for missing user in `dev` | `dev` | High | `404` with `{ "error": "..." }` | `test_error_responses_follow_contract[get-missing-user]` |
| TC-050 | Error contract | `GET /users/{email}` | Error schema for missing user in `prod` | `prod` | High | `404` with `{ "error": "..." }` | `test_error_responses_follow_contract[get-missing-user]` |
| TC-051 | Error contract | `PUT /users/{email}` | Error schema for updating missing user in `dev` | `dev` | Medium | `404` with `{ "error": "..." }` | `test_error_responses_follow_contract[update missing user-_update_missing_user_response-tc_ids3]` |
| TC-052 | Error contract | `PUT /users/{email}` | Error schema for updating missing user in `prod` | `prod` | Medium | `404` with `{ "error": "..." }` | `test_error_responses_follow_contract[update missing user-_update_missing_user_response-tc_ids3]` |
| TC-053 | Error contract | `DELETE /users/{email}` | Error schema for deleting missing user in `dev` | `dev` | Medium | `404` with `{ "error": "..." }` | `test_error_responses_follow_contract[delete missing user-_delete_missing_user_response-tc_ids4]` |
| TC-054 | Error contract | `DELETE /users/{email}` | Error schema for deleting missing user in `prod` | `prod` | Medium | `404` with `{ "error": "..." }` | `test_error_responses_follow_contract[delete missing user-_delete_missing_user_response-tc_ids4]` |
| TC-055 | Error contract | `DELETE /users/{email}` | Error schema for unauthorized delete in `dev` | `dev` | High | `401` with `{ "error": "..." }` | `test_error_responses_follow_contract[delete-unauthorized]` |
| TC-056 | Error contract | `DELETE /users/{email}` | Error schema for unauthorized delete in `prod` | `prod` | High | `401` with `{ "error": "..." }` | `test_error_responses_follow_contract[delete-unauthorized]` |

## Notes

- `dev` and `prod` are both exercised by the same automated suite through environment-specific runs in local execution and GitHub Actions.
- Some negative scenarios are expected to fail today because the current application behavior does not match the OpenAPI specification; those mismatches are documented in `docs/bug_report.md`.
- Contract-focused rows are intentionally split per environment so the matrix reflects what the challenge explicitly asks for: testing both `dev` and `prod`.

## Additional Scenarios With More Time

- Add explicit malformed JSON body tests for `POST /users` and `PUT /users/{email}` to validate parser-level error handling.
- Add path-encoding edge cases for `GET`, `PUT`, and `DELETE` using emails with `+`, uppercase characters, or percent-encoded values.
- Add exploratory negative cases for invalid email format in the path parameter of `GET`, `PUT`, and `DELETE`. The OpenAPI spec constrains the path as `format: email`, but it does not define the expected error status for malformed path values, so these are better treated as exploratory coverage than hard contract assertions.
- Add repeated-delete coverage to verify whether deleting the same user twice should consistently transition from `204` to `404`.
- Add stronger bidirectional isolation checks with setup and verification starting from both `dev` and `prod`.
- Add tests for response schema drift on successful `POST`, `GET`, `PUT`, and collection `GET` responses beyond the current core field validation.
- Add auth-header robustness tests, such as whitespace-only tokens, missing header casing variants, and unexpected auth header values on unprotected endpoints.
- Extend cleanup protections with optional environment-reset hooks if the service ever exposes administrative teardown endpoints.
- Add workflow-level publishing of JUnit XML into the GitHub Actions test summary for easier inspection directly in CI.
