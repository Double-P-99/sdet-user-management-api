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

import pytest

pytestmark = [pytest.mark.api, pytest.mark.regression]
BUG_REPORT_REF = "documented in docs/bug_report.md"


@pytest.mark.smoke
@pytest.mark.e2e_id("E2E-002")
@pytest.mark.tc_id("TC-020", "TC-021")
def test_get_user_returns_200_for_existing_user(
    users_client: UsersClient, create_user_payload: CreateUserRequest
) -> None:
    """TC-020/TC-021: fetch an existing user by email and validate the success schema."""
    create_response = users_client.create_user(create_user_payload)
    get_response = users_client.get_user(create_user_payload.email)

    assert_status_code(create_response, 201)
    assert_status_code(get_response, 200)
    assert_json_content_type(get_response)
    body = get_response.json()
    assert_user_shape(body)
    assert body == create_user_payload.to_dict()


@pytest.mark.tc_id("TC-022", "TC-023")
@pytest.mark.xfail(
    reason=f"Known bug BUG-003: missing user lookup returns 500 instead of 404; {BUG_REPORT_REF}",
    strict=False,
)
def test_get_user_returns_404_for_unknown_user(users_client: UsersClient) -> None:
    """TC-022/TC-023: return not found when fetching a user that does not exist."""
    response = users_client.get_user("missing.user@example.com")

    assert_status_code(response, 404)
    assert_error_response(response)
