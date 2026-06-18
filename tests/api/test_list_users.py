"""Tests for GET /users behavior."""

from __future__ import annotations

import pytest

from api.users_client import UsersClient
from models.user import CreateUserRequest
from validators.api_validators import (
    assert_json_content_type,
    assert_status_code,
    assert_user_list_contains_exactly_once,
    assert_user_list_shape,
    assert_user_payload,
)

pytestmark = [pytest.mark.api, pytest.mark.regression]


@pytest.mark.smoke
@pytest.mark.e2e_id("E2E-001")
@pytest.mark.tc_id("TC-001", "TC-002")
def test_list_users_returns_200_and_json_array(users_client: UsersClient) -> None:
    """TC-001/TC-002: list users and validate the collection response shape."""
    response = users_client.list_users()

    assert_status_code(response, 200)
    assert_json_content_type(response)
    assert_user_list_shape(response.json())


@pytest.mark.e2e_id("E2E-003")
@pytest.mark.tc_id("TC-003", "TC-004", "TC-005", "TC-006")
def test_list_users_includes_created_user(
    users_client: UsersClient, create_user_payload: CreateUserRequest
) -> None:
    """TC-003/TC-004/TC-005/TC-006: created users appear in the collection and every item matches the User schema."""
    create_response = users_client.create_user(create_user_payload)
    list_response = users_client.list_users()

    assert_status_code(create_response, 201)
    assert_status_code(list_response, 200)
    assert_user_list_contains_exactly_once(
        list_response.json(),
        create_user_payload.to_dict(),
    )


@pytest.mark.e2e_id("E2E-010")
def test_get_user_and_list_user_entry_match_after_create(
    users_client: UsersClient, create_user_payload: CreateUserRequest
) -> None:
    """The single-user view and collection view should agree after creation."""
    create_response = users_client.create_user(create_user_payload)
    get_response = users_client.get_user(create_user_payload.email)
    list_response = users_client.list_users()

    assert_status_code(create_response, 201)
    assert_status_code(get_response, 200)
    assert_status_code(list_response, 200)
    assert_json_content_type(get_response)
    assert_json_content_type(list_response)

    get_body = assert_user_payload(
        get_response.json(),
        create_user_payload.to_dict(),
    )
    listed_user = assert_user_list_contains_exactly_once(
        list_response.json(),
        create_user_payload.to_dict(),
    )
    assert get_body == listed_user == create_user_payload.to_dict()
