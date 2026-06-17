"""Contract tests for API error responses."""

from __future__ import annotations

import os

import pytest

from api.users_client import UsersClient
from factories.user_factory import UserFactory
from validators.api_validators import assert_error_response, assert_status_code


pytestmark = [pytest.mark.api, pytest.mark.contract, pytest.mark.regression]
BUG_REPORT_REF = "documented in docs/bug_report.md"
IS_DEV = os.getenv("TEST_ENV", "dev") == "dev"


def _duplicate_create_response(users_client: UsersClient):
    payload = UserFactory.build_create_user()
    users_client.create_user(payload)
    return users_client.create_user(payload)


def _create_user_validation_error_response(users_client: UsersClient):
    return users_client.create_user_raw(UserFactory.invalid_email_payload())


def _get_missing_user_response(users_client: UsersClient):
    return users_client.get_user("missing.user@example.com")


def _update_missing_user_response(users_client: UsersClient):
    return users_client.update_user(
        "missing.user@example.com",
        UserFactory.build_update_user(),
    )


def _delete_missing_user_response(users_client: UsersClient):
    return users_client.delete_user("missing.user@example.com")


def _unauthorized_delete_response(users_client: UsersClient):
    payload = UserFactory.build_create_user()
    users_client.create_user(payload)
    return users_client.delete_user(payload.email, auth_token="")


@pytest.mark.tc_id(
    "TC-045",
    "TC-046",
    "TC-047",
    "TC-048",
    "TC-049",
    "TC-050",
    "TC-051",
    "TC-052",
    "TC-053",
    "TC-054",
    "TC-055",
    "TC-056",
)
@pytest.mark.parametrize(
    ("description", "response", "tc_ids"),
    [
        pytest.param(
            "create user validation error",
            _create_user_validation_error_response,
            ("TC-045", "TC-046"),
            id="create-user-validation-error",
            marks=pytest.mark.xfail(
                reason=f"Known bug BUG-001: invalid email create does not return documented error; {BUG_REPORT_REF}",
                strict=False,
            ),
        ),
        pytest.param(
            "create user duplicate email",
            _duplicate_create_response,
            ("TC-047", "TC-048"),
            id="create-user-duplicate-email",
            marks=pytest.mark.xfail(
                reason=f"Known bug BUG-002: duplicate create returns 500 instead of 409; {BUG_REPORT_REF}",
                strict=False,
            ),
        ),
        pytest.param(
            "get missing user",
            _get_missing_user_response,
            ("TC-049", "TC-050"),
            id="get-missing-user",
            marks=pytest.mark.xfail(
                reason=f"Known bug BUG-003: missing user lookup returns 500 instead of 404; {BUG_REPORT_REF}",
                strict=False,
            ),
        ),
        (
            "update missing user",
            _update_missing_user_response,
            ("TC-051", "TC-052"),
        ),
        (
            "delete missing user",
            _delete_missing_user_response,
            ("TC-053", "TC-054"),
        ),
        pytest.param(
            "delete unauthorized",
            _unauthorized_delete_response,
            ("TC-055", "TC-056"),
            id="delete-unauthorized",
            marks=pytest.mark.xfail(
                IS_DEV,
                reason=f"Known bug BUG-004: dev delete without auth does not return documented error; {BUG_REPORT_REF}",
                strict=False,
            ),
        ),
    ],
)
def test_error_responses_follow_contract(
    users_client: UsersClient, description: str, response, tc_ids: tuple[str, str]
) -> None:
    """TC-045..TC-056: validate documented error status codes and ErrorResponse schema across endpoints."""
    result = response(users_client)

    assert result.status_code in {400, 401, 404, 409}, (
        f"{description} produced unexpected status {result.status_code}"
    )
    assert_error_response(result)
