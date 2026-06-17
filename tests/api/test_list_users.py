"""Tests for GET /users behavior."""

from __future__ import annotations

from api.users_client import UsersClient
from models.user import CreateUserRequest
from validators.api_validators import (
    assert_json_content_type,
    assert_status_code,
    assert_user_shape,
)


def test_list_users_returns_200_and_json_array(users_client: UsersClient) -> None:
    response = users_client.list_users()

    assert_status_code(response, 200)
    assert_json_content_type(response)
    body = response.json()
    assert isinstance(body, list), f"Expected list body, got {type(body).__name__}"


def test_list_users_includes_created_user(
    users_client: UsersClient, create_user_payload: CreateUserRequest
) -> None:
    create_response = users_client.create_user(create_user_payload)
    list_response = users_client.list_users()

    assert_status_code(create_response, 201)
    assert_status_code(list_response, 200)
    users = list_response.json()
    assert isinstance(users, list)
    assert any(user.get("email") == create_user_payload.email for user in users)
    for user in users:
        assert_user_shape(user)
