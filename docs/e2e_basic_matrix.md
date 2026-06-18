# Basic E2E Matrix

This matrix complements `docs/test_matrix.md` with a smaller set of end-to-end workflow scenarios.

The goal here is not to restate every contract permutation, but to protect the most important user journeys and the read-after-write behaviors that tend to expose real product bugs.

| E2E ID | Workflow | Environment | Expected Result | Current Automated Coverage | Notes |
| --- | --- | --- | --- | --- | --- |
| E2E-001 | List users with no setup | `dev`, `prod` | `GET /users` returns `200` and a JSON array | `test_list_users_returns_200_and_json_array` | Marked with `@pytest.mark.e2e_id("E2E-001")` |
| E2E-002 | Create user and fetch by email | `dev`, `prod` | `POST` returns `201`; `GET /users/{email}` returns the same user | `test_get_user_returns_200_for_existing_user` | Marked with `@pytest.mark.e2e_id("E2E-002")` |
| E2E-003 | Create user and verify it appears in list | `dev`, `prod` | `GET /users` includes the created email and valid `User` items | `test_list_users_includes_created_user` | Marked with `@pytest.mark.e2e_id("E2E-003")` |
| E2E-004 | Create, update, and fetch by updated email | `dev`, `prod` | `PUT` returns `200`; follow-up `GET /users/{new_email}` returns updated user | `test_update_user_persists_changes_for_followup_get` | Marked with `@pytest.mark.e2e_id("E2E-004")`; currently exposes `BUG-006` |
| E2E-005 | Create, update with same email, and verify in list | `dev`, `prod` | `PUT` returns `200`; `GET /users` shows updated `name` and `age` for that email | `test_update_user_persists_field_changes_in_user_list_when_email_is_unchanged` | Marked with `@pytest.mark.e2e_id("E2E-005")`; currently exposes `BUG-006` |
| E2E-006 | Create and delete with valid auth | `dev`, `prod` | `DELETE` returns `204` | `test_delete_user_returns_204_for_existing_user` | Marked with `@pytest.mark.e2e_id("E2E-006")` |
| E2E-007 | Create, delete, then update | `dev`, `prod` | update after delete returns `404` | `test_update_user_returns_404_after_user_was_deleted` | Marked with `@pytest.mark.e2e_id("E2E-007")` |
| E2E-008 | Create in one environment and verify isolation from the other | Cross-environment | secondary environment does not expose the user | `test_users_are_isolated_between_environments` | Marked with `@pytest.mark.e2e_id("E2E-008")` |

## Why This Matrix Exists

- The full matrix in `docs/test_matrix.md` gives complete traceability to the OpenAPI contract.
- This basic E2E matrix highlights the smallest set of workflows that should keep catching real application bugs even if individual endpoint tests still pass.
- Bugs like failed `PUT` persistence are easier to surface in workflow tests than in isolated request/response checks.

## Scope Guidance

- Keep this matrix small and workflow-oriented.
- Add a new row only when the scenario represents a real user journey or a read-after-write consistency check.
- Do not move framework-only tests here. Internal cleanup or client-tracking behavior belongs in unit tests, not in the basic E2E matrix.
