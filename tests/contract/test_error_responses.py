"""Contract tests for API error responses."""

from __future__ import annotations

import pytest

from api.users_client import UsersClient
from factories.user_factory import UserFactory
from validators.api_validators import assert_error_response, assert_status_code


@pytest.mark.contract
@pytest.mark.parametrize(
    ("description", "response"),
    [
        (
            "create user validation error",
            lambda client: client.create_user_raw(UserFactory.invalid_email_payload()),
        ),
        (
            "create user duplicate email",
            lambda client: _duplicate_create_response(client),
        ),
        (
            "get missing user",
            lambda client: client.get_user("missing.user@example.com"),
        ),
        (
            "update missing user",
            lambda client: client.update_user(
                "missing.user@example.com",
                UserFactory.build_update_user(),
            ),
        ),
        (
            "delete missing user",
            lambda client: client.delete_user("missing.user@example.com"),
        ),
        (
            "delete unauthorized",
            lambda client: _unauthorized_delete_response(client),
        ),
    ],
)
def test_error_responses_follow_contract(
    users_client: UsersClient, description: str, response
) -> None:
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
