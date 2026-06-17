"""Tests for dev/prod environment isolation."""

from __future__ import annotations

from api.users_client import UsersClient
from factories.user_factory import UserFactory
from validators.api_validators import assert_status_code


def test_users_are_isolated_between_environments(
    users_client: UsersClient, secondary_users_client: UsersClient
) -> None:
    payload = UserFactory.build_create_user()

    create_response = users_client.create_user(payload)
    primary_get_response = users_client.get_user(payload.email)
    secondary_get_response = secondary_users_client.get_user(payload.email)

    assert_status_code(create_response, 201)
    assert_status_code(primary_get_response, 200)
    assert_status_code(secondary_get_response, 404)
