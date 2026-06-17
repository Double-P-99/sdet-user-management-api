"""Tests for PUT /users/{email} behavior."""

from __future__ import annotations

import pytest

from api.users_client import UsersClient
from factories.user_factory import UserFactory, UserOverrides
from models.user import CreateUserRequest, UpdateUserRequest
from validators.api_validators import (
    assert_error_response,
    assert_json_content_type,
    assert_status_code,
    assert_user_shape,
)


def test_update_user_returns_200_and_updated_user(
    users_client: UsersClient,
    create_user_payload: CreateUserRequest,
    update_user_payload: UpdateUserRequest,
) -> None:
    create_response = users_client.create_user(create_user_payload)
    update_response = users_client.update_user(create_user_payload.email, update_user_payload)

    assert_status_code(create_response, 201)
    assert_status_code(update_response, 200)
    assert_json_content_type(update_response)
    body = update_response.json()
    assert_user_shape(body)
    assert body == update_user_payload.to_dict()


@pytest.mark.parametrize("missing_field", ["name", "email", "age"])
def test_update_user_returns_400_for_missing_required_fields(
    users_client: UsersClient,
    create_user_payload: CreateUserRequest,
    missing_field: str,
) -> None:
    users_client.create_user(create_user_payload)

    response = users_client.update_user_raw(
        create_user_payload.email,
        UserFactory.missing_field_payload(missing_field),
    )

    assert_status_code(response, 400)
    assert_error_response(response)


def test_update_user_returns_400_for_invalid_email(
    users_client: UsersClient, create_user_payload: CreateUserRequest
) -> None:
    users_client.create_user(create_user_payload)

    response = users_client.update_user_raw(
        create_user_payload.email,
        UserFactory.invalid_email_payload(),
    )

    assert_status_code(response, 400)
    assert_error_response(response)


def test_update_user_returns_404_for_unknown_user(
    users_client: UsersClient, update_user_payload: UpdateUserRequest
) -> None:
    response = users_client.update_user("missing.user@example.com", update_user_payload)

    assert_status_code(response, 404)
    assert_error_response(response)


def test_update_user_returns_409_for_duplicate_email(users_client: UsersClient) -> None:
    original_user = UserFactory.build_create_user()
    another_user = UserFactory.build_create_user()
    duplicate_email_payload = UserFactory.build_update_user(
        overrides=UserOverrides(email=another_user.email, age=31)
    )

    users_client.create_user(original_user)
    users_client.create_user(another_user)

    response = users_client.update_user(original_user.email, duplicate_email_payload)

    assert_status_code(response, 409)
    assert_error_response(response)
