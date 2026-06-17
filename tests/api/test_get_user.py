"""Tests for GET /users/{email} behavior."""

from __future__ import annotations

from api.users_client import UsersClient
from factories.user_factory import UserFactory
from models.user import CreateUserRequest
from validators.api_validators import (
    assert_error_response,
    assert_json_content_type,
    assert_status_code,
    assert_user_shape,
)


def test_get_user_returns_200_for_existing_user(
    users_client: UsersClient, create_user_payload: CreateUserRequest
) -> None:
    create_response = users_client.create_user(create_user_payload)
    get_response = users_client.get_user(create_user_payload.email)

    assert_status_code(create_response, 201)
    assert_status_code(get_response, 200)
    assert_json_content_type(get_response)
    body = get_response.json()
    assert_user_shape(body)
    assert body == create_user_payload.to_dict()


def test_get_user_returns_404_for_unknown_user(users_client: UsersClient) -> None:
    response = users_client.get_user("missing.user@example.com")

    assert_status_code(response, 404)
    assert_error_response(response)
