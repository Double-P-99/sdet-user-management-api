"""Tests for DELETE /users/{email} behavior."""

from __future__ import annotations

from api.users_client import UsersClient
from factories.user_factory import UserFactory
from models.user import CreateUserRequest
from validators.api_validators import assert_error_response, assert_status_code


def test_delete_user_returns_204_for_existing_user(
    users_client: UsersClient, create_user_payload: CreateUserRequest
) -> None:
    create_response = users_client.create_user(create_user_payload)
    delete_response = users_client.delete_user(create_user_payload.email)

    assert_status_code(create_response, 201)
    assert_status_code(delete_response, 204)
    assert delete_response.text == ""


def test_delete_user_returns_401_without_auth_header(users_client: UsersClient) -> None:
    payload = UserFactory.build_create_user()
    users_client.create_user(payload)

    response = users_client.delete_user(payload.email, auth_token="")

    assert_status_code(response, 401)
    assert_error_response(response)


def test_delete_user_returns_401_for_invalid_auth_token(users_client: UsersClient) -> None:
    payload = UserFactory.build_create_user()
    users_client.create_user(payload)

    response = users_client.delete_user(payload.email, auth_token="wrong-token")

    assert_status_code(response, 401)
    assert_error_response(response)


def test_delete_user_returns_404_for_unknown_user(users_client: UsersClient) -> None:
    response = users_client.delete_user("missing.user@example.com")

    assert_status_code(response, 404)
    assert_error_response(response)
