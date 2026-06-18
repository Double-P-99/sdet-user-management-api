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
BUG_REPORT_REF = "documented in docs/bug_report.md"


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


@pytest.mark.xfail(
    reason=f"Known bug BUG-006: successful update responses do not persist user changes reliably; {BUG_REPORT_REF}",
    strict=False,
)
@pytest.mark.e2e_id("E2E-004")
@pytest.mark.tc_id("TC-024")
def test_update_user_persists_changes_for_followup_get(
    users_client: UsersClient,
    create_user_payload: CreateUserRequest,
    update_user_payload: UpdateUserRequest,
) -> None:
    """Ensure a successful update is visible in a subsequent fetch."""
    create_response = users_client.create_user(create_user_payload)
    update_response = users_client.update_user(create_user_payload.email, update_user_payload)
    get_response = users_client.get_user(update_user_payload.email)

    assert_status_code(create_response, 201)
    assert_status_code(update_response, 200)
    assert_status_code(get_response, 200)
    assert_json_content_type(get_response)
    body = get_response.json()
    assert_user_shape(body)
    assert body == update_user_payload.to_dict()


@pytest.mark.xfail(
    reason=f"Known bug BUG-006: successful update responses do not persist user changes reliably; {BUG_REPORT_REF}",
    strict=False,
)
@pytest.mark.e2e_id("E2E-005")
@pytest.mark.tc_id("TC-057", "TC-058")
def test_update_user_persists_field_changes_in_user_list_when_email_is_unchanged(
    users_client: UsersClient,
    create_user_payload: CreateUserRequest,
) -> None:
    """Ensure list results reflect updated fields when the email stays the same."""
    update_user_payload = UserFactory.build_update_user(
        overrides=UserOverrides(
            email=create_user_payload.email,
            name=f"{create_user_payload.name} Updated",
            age=create_user_payload.age + 1,
        )
    )

    create_response = users_client.create_user(create_user_payload)
    update_response = users_client.update_user(create_user_payload.email, update_user_payload)
    list_response = users_client.list_users()

    assert_status_code(create_response, 201)
    assert_status_code(update_response, 200)
    assert_status_code(list_response, 200)
    assert_json_content_type(list_response)
    users = list_response.json()
    matching_users = [user for user in users if user.get("email") == create_user_payload.email]

    assert len(matching_users) == 1, (
        f"Expected one user with email {create_user_payload.email}, got {len(matching_users)}"
    )
    assert_user_shape(matching_users[0])
    assert matching_users[0] == update_user_payload.to_dict()


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


@pytest.mark.e2e_id("E2E-007")
def test_update_user_returns_404_after_user_was_deleted(
    users_client: UsersClient,
    create_user_payload: CreateUserRequest,
    update_user_payload: UpdateUserRequest,
) -> None:
    """A deleted user should no longer accept update operations."""
    create_response = users_client.create_user(create_user_payload)
    delete_response = users_client.delete_user(create_user_payload.email)
    update_response = users_client.update_user(create_user_payload.email, update_user_payload)

    assert_status_code(create_response, 201)
    assert_status_code(delete_response, 204)
    assert_status_code(update_response, 404)
    assert_error_response(update_response)


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
