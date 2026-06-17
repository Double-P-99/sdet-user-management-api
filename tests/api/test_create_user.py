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

pytestmark = [pytest.mark.api, pytest.mark.regression]
BUG_REPORT_REF = "documented in docs/bug_report.md"


@pytest.mark.smoke
@pytest.mark.tc_id("TC-007", "TC-008")
def test_create_user_returns_201_and_created_user(
    users_client: UsersClient, create_user_payload: CreateUserRequest
) -> None:
    """TC-007/TC-008: create a user with a valid payload and validate the success response."""
    response = users_client.create_user(create_user_payload)

    assert_status_code(response, 201)
    assert_json_content_type(response)
    body = response.json()
    assert_user_shape(body)
    assert body == create_user_payload.to_dict()


@pytest.mark.tc_id("TC-009", "TC-010", "TC-011")
@pytest.mark.parametrize(
    ("missing_field", "tc_id"),
    [
        pytest.param("name", "TC-009", id="TC-009"),
        pytest.param("email", "TC-010", id="TC-010"),
        pytest.param("age", "TC-011", id="TC-011"),
    ],
)
def test_create_user_returns_400_for_missing_required_fields(
    users_client: UsersClient, missing_field: str, tc_id: str
) -> None:
    """TC-009/TC-010/TC-011: reject create-user requests missing required fields."""
    response = users_client.create_user_raw(UserFactory.missing_field_payload(missing_field))

    assert_status_code(response, 400)
    assert_error_response(response)


@pytest.mark.tc_id("TC-012", "TC-013", "TC-014", "TC-015")
@pytest.mark.parametrize(
    ("age", "tc_id"),
    [
        pytest.param(0, "TC-012", id="TC-012"),
        pytest.param(-1, "TC-013", id="TC-013"),
        pytest.param(151, "TC-014", id="TC-014"),
        pytest.param("thirty", "TC-015", id="TC-015"),
    ],
)
def test_create_user_returns_400_for_invalid_age(
    users_client: UsersClient, age: object, tc_id: str
) -> None:
    """TC-012/TC-013/TC-014/TC-015: reject create-user requests with invalid age values."""
    response = users_client.create_user_raw(UserFactory.invalid_age_payload(age))

    assert_status_code(response, 400)
    assert_error_response(response)


@pytest.mark.tc_id("TC-016", "TC-017")
@pytest.mark.xfail(
    reason=f"Known bug BUG-001: invalid email is accepted during create-user; {BUG_REPORT_REF}",
    strict=False,
)
def test_create_user_returns_400_for_invalid_email(users_client: UsersClient) -> None:
    """TC-016/TC-017: reject create-user requests with invalid email format."""
    response = users_client.create_user_raw(UserFactory.invalid_email_payload())

    assert_status_code(response, 400)
    assert_error_response(response)


@pytest.mark.tc_id("TC-018", "TC-019")
@pytest.mark.xfail(
    reason=f"Known bug BUG-002: duplicate create returns 500 instead of 409; {BUG_REPORT_REF}",
    strict=False,
)
def test_create_user_returns_409_for_duplicate_email(users_client: UsersClient) -> None:
    """TC-018/TC-019: reject create-user requests when the email already exists."""
    payload = UserFactory.build_create_user()

    first_response = users_client.create_user(payload)
    duplicate_response = users_client.create_user(payload)

    assert_status_code(first_response, 201)
    assert_status_code(duplicate_response, 409)
    assert_error_response(duplicate_response)
