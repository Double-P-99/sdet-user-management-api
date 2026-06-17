"""Tests for DELETE /users/{email} behavior."""

from __future__ import annotations

import pytest

from api.users_client import UsersClient
from factories.user_factory import UserFactory
from models.user import CreateUserRequest
from validators.api_validators import assert_error_response, assert_status_code

pytestmark = [pytest.mark.api, pytest.mark.regression]


@pytest.mark.smoke
@pytest.mark.security
@pytest.mark.tc_id("TC-035", "TC-036")
def test_delete_user_returns_204_for_existing_user(
    users_client: UsersClient, create_user_payload: CreateUserRequest
) -> None:
    """TC-035/TC-036: delete an existing user with valid authentication."""
    create_response = users_client.create_user(create_user_payload)
    delete_response = users_client.delete_user(create_user_payload.email)

    assert_status_code(create_response, 201)
    assert_status_code(delete_response, 204)
    assert delete_response.text == ""


@pytest.mark.security
@pytest.mark.tc_id("TC-037", "TC-038")
def test_delete_user_returns_401_without_auth_header(users_client: UsersClient) -> None:
    """TC-037/TC-038: reject delete requests that omit the authentication header."""
    payload = UserFactory.build_create_user()
    users_client.create_user(payload)

    response = users_client.delete_user(payload.email, auth_token="")

    assert_status_code(response, 401)
    assert_error_response(response)


@pytest.mark.security
@pytest.mark.tc_id("TC-039", "TC-040")
def test_delete_user_returns_401_for_invalid_auth_token(users_client: UsersClient) -> None:
    """TC-039/TC-040: reject delete requests with an invalid authentication token."""
    payload = UserFactory.build_create_user()
    users_client.create_user(payload)

    response = users_client.delete_user(payload.email, auth_token="wrong-token")

    assert_status_code(response, 401)
    assert_error_response(response)


@pytest.mark.tc_id("TC-041", "TC-042")
def test_delete_user_returns_404_for_unknown_user(users_client: UsersClient) -> None:
    """TC-041/TC-042: return not found when deleting a user that does not exist."""
    response = users_client.delete_user("missing.user@example.com")

    assert_status_code(response, 404)
    assert_error_response(response)
