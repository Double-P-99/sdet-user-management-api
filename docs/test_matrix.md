# Test Matrix

Map each OpenAPI endpoint and status code to one or more automated tests.

| Endpoint | Method | Expected Status | Covered By |
| --- | --- | --- | --- |
| `/users` | `GET` | `200` | `tests/api/test_list_users.py` |
| `/users` | `POST` | `201` | `tests/api/test_create_user.py` |
| `/users` | `POST` | `400` | `tests/api/test_create_user.py`, `tests/contract/test_error_responses.py` |
| `/users` | `POST` | `409` | `tests/api/test_create_user.py`, `tests/contract/test_error_responses.py` |
| `/users/{email}` | `GET` | `200` | `tests/api/test_get_user.py` |
| `/users/{email}` | `GET` | `404` | `tests/api/test_get_user.py`, `tests/contract/test_error_responses.py` |
| `/users/{email}` | `PUT` | `200` | `tests/api/test_update_user.py` |
| `/users/{email}` | `PUT` | `400` | `tests/api/test_update_user.py` |
| `/users/{email}` | `PUT` | `404` | `tests/api/test_update_user.py`, `tests/contract/test_error_responses.py` |
| `/users/{email}` | `PUT` | `409` | `tests/api/test_update_user.py` |
| `/users/{email}` | `DELETE` | `204` | `tests/api/test_delete_user.py` |
| `/users/{email}` | `DELETE` | `401` | `tests/api/test_delete_user.py`, `tests/contract/test_error_responses.py` |
| `/users/{email}` | `DELETE` | `404` | `tests/api/test_delete_user.py`, `tests/contract/test_error_responses.py` |
| `/dev` vs `/prod` | Isolation | `200/404` | `tests/api/test_environment_isolation.py` |
