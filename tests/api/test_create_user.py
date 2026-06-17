"""Tests for POST /users behavior."""

from __future__ import annotations

import pytest

from api.users_client import UsersClient
from factories.user_factory import UserFactory
from models.user import CreateUserRequest
from validators.api_validators import (
    assert_error_response,
    assert_json_content_type,
    assert_status_code,
    assert_user_shape,
)


def test_create_user_returns_201_and_created_user(
    users_client: UsersClient, create_user_payload: CreateUserRequest
) -> None:
    response = users_client.create_user(create_user_payload)

    assert_status_code(response, 201)
    assert_json_content_type(response)
    body = response.json()
    assert_user_shape(body)
    assert body == create_user_payload.to_dict()


@pytest.mark.parametrize("missing_field", ["name", "email", "age"])
def test_create_user_returns_400_for_missing_required_fields(
    users_client: UsersClient, missing_field: str
) -> None:
    response = users_client.create_user_raw(UserFactory.missing_field_payload(missing_field))

    assert_status_code(response, 400)
    assert_error_response(response)


@pytest.mark.parametrize("age", [0, 151, -1, "thirty"])
def test_create_user_returns_400_for_invalid_age(
    users_client: UsersClient, age: object
) -> None:
    response = users_client.create_user_raw(UserFactory.invalid_age_payload(age))

    assert_status_code(response, 400)
    assert_error_response(response)


def test_create_user_returns_400_for_invalid_email(users_client: UsersClient) -> None:
    response = users_client.create_user_raw(UserFactory.invalid_email_payload())

    assert_status_code(response, 400)
    assert_error_response(response)


def test_create_user_returns_409_for_duplicate_email(users_client: UsersClient) -> None:
    payload = UserFactory.build_create_user()

    first_response = users_client.create_user(payload)
    duplicate_response = users_client.create_user(payload)

    assert_status_code(first_response, 201)
    assert_status_code(duplicate_response, 409)
    assert_error_response(duplicate_response)
