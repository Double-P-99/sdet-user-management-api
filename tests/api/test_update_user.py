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

pytestmark = [pytest.mark.api, pytest.mark.regression]


@pytest.mark.smoke
@pytest.mark.tc_id("TC-024", "TC-025")
def test_update_user_returns_200_and_updated_user(
    users_client: UsersClient,
    create_user_payload: CreateUserRequest,
    update_user_payload: UpdateUserRequest,
) -> None:
    """TC-024/TC-025: update an existing user and validate the updated User response."""
    create_response = users_client.create_user(create_user_payload)
    update_response = users_client.update_user(create_user_payload.email, update_user_payload)

    assert_status_code(create_response, 201)
    assert_status_code(update_response, 200)
    assert_json_content_type(update_response)
    body = update_response.json()
    assert_user_shape(body)
    assert body == update_user_payload.to_dict()


@pytest.mark.tc_id("TC-026", "TC-027", "TC-028")
@pytest.mark.parametrize(
    ("missing_field", "tc_id"),
    [
        pytest.param("name", "TC-026", id="TC-026"),
        pytest.param("email", "TC-027", id="TC-027"),
        pytest.param("age", "TC-028", id="TC-028"),
    ],
)
def test_update_user_returns_400_for_missing_required_fields(
    users_client: UsersClient,
    create_user_payload: CreateUserRequest,
    missing_field: str,
    tc_id: str,
) -> None:
    """TC-026/TC-027/TC-028: reject update requests missing required fields."""
    users_client.create_user(create_user_payload)

    response = users_client.update_user_raw(
        create_user_payload.email,
        UserFactory.missing_field_payload(missing_field),
    )

    assert_status_code(response, 400)
    assert_error_response(response)


@pytest.mark.tc_id("TC-029", "TC-030")
def test_update_user_returns_400_for_invalid_email(
    users_client: UsersClient, create_user_payload: CreateUserRequest
) -> None:
    """TC-029/TC-030: reject update requests with invalid email format."""
    users_client.create_user(create_user_payload)

    response = users_client.update_user_raw(
        create_user_payload.email,
        UserFactory.invalid_email_payload(),
    )

    assert_status_code(response, 400)
    assert_error_response(response)


@pytest.mark.tc_id("TC-031", "TC-032")
def test_update_user_returns_404_for_unknown_user(
    users_client: UsersClient, update_user_payload: UpdateUserRequest
) -> None:
    """TC-031/TC-032: return not found when updating a user that does not exist."""
    response = users_client.update_user("missing.user@example.com", update_user_payload)

    assert_status_code(response, 404)
    assert_error_response(response)


@pytest.mark.tc_id("TC-033", "TC-034")
def test_update_user_returns_409_for_duplicate_email(users_client: UsersClient) -> None:
    """TC-033/TC-034: reject updates that attempt to reuse another user's email."""
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
