"""Contract tests for API error responses."""

from __future__ import annotations

import pytest

from api.users_client import UsersClient
from factories.user_factory import UserFactory
from validators.api_validators import assert_error_response, assert_status_code


pytestmark = [pytest.mark.api, pytest.mark.contract, pytest.mark.regression]


@pytest.mark.tc_id(
    "TC-045",
    "TC-046",
    "TC-047",
    "TC-048",
    "TC-049",
    "TC-050",
    "TC-051",
    "TC-052",
    "TC-053",
    "TC-054",
    "TC-055",
    "TC-056",
)
@pytest.mark.parametrize(
    ("description", "response", "tc_ids"),
    [
        (
            "create user validation error",
            lambda client: client.create_user_raw(UserFactory.invalid_email_payload()),
            ("TC-045", "TC-046"),
        ),
        (
            "create user duplicate email",
            lambda client: _duplicate_create_response(client),
            ("TC-047", "TC-048"),
        ),
        (
            "get missing user",
            lambda client: client.get_user("missing.user@example.com"),
            ("TC-049", "TC-050"),
        ),
        (
            "update missing user",
            lambda client: client.update_user(
                "missing.user@example.com",
                UserFactory.build_update_user(),
            ),
            ("TC-051", "TC-052"),
        ),
        (
            "delete missing user",
            lambda client: client.delete_user("missing.user@example.com"),
            ("TC-053", "TC-054"),
        ),
        (
            "delete unauthorized",
            lambda client: _unauthorized_delete_response(client),
            ("TC-055", "TC-056"),
        ),
    ],
)
def test_error_responses_follow_contract(
    users_client: UsersClient, description: str, response, tc_ids: tuple[str, str]
) -> None:
    """TC-045..TC-056: validate documented error status codes and ErrorResponse schema across endpoints."""
    result = response(users_client)

    assert result.status_code in {400, 401, 404, 409}, (
        f"{description} produced unexpected status {result.status_code}"
    )
    assert_error_response(result)


def _duplicate_create_response(users_client: UsersClient):
    payload = UserFactory.build_create_user()
    users_client.create_user(payload)
    return users_client.create_user(payload)


def _unauthorized_delete_response(users_client: UsersClient):
    payload = UserFactory.build_create_user()
    users_client.create_user(payload)
    return users_client.delete_user(payload.email, auth_token="")
