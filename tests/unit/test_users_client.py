"""Unit tests for the resource-level user client."""

from __future__ import annotations

from unittest.mock import Mock

import pytest

from api.users_client import UsersClient
from config.settings import Settings
from models.user import CreateUserRequest, UpdateUserRequest


pytestmark = [pytest.mark.unit]


def _settings() -> Settings:
    return Settings(
        base_url="http://localhost:3000",
        environment="dev",
        auth_token="mysecrettoken",
        timeout=10.0,
    )


def _response(status_code: int) -> Mock:
    response = Mock()
    response.status_code = status_code
    return response


def test_delete_user_uses_default_auth_and_encoded_email() -> None:
    session = Mock()
    session.request.return_value = _response(204)
    client = UsersClient(_settings(), session=session)

    client.delete_user("test+user@example.com")

    session.request.assert_called_once_with(
        method="DELETE",
        url="http://localhost:3000/dev/users/test%2Buser%40example.com",
        headers={"Authentication": "mysecrettoken"},
        json=None,
        params=None,
        timeout=10.0,
    )


def test_create_user_tracks_successfully_created_email() -> None:
    session = Mock()
    session.request.return_value = _response(201)
    client = UsersClient(_settings(), session=session)
    payload = CreateUserRequest(name="Jane", email="jane@example.com", age=30)

    client.create_user(payload)

    assert client.tracked_user_emails() == ("jane@example.com",)


def test_create_user_does_not_track_failed_creation() -> None:
    session = Mock()
    session.request.return_value = _response(500)
    client = UsersClient(_settings(), session=session)
    payload = CreateUserRequest(name="Jane", email="jane@example.com", age=30)

    client.create_user(payload)

    assert client.tracked_user_emails() == ()


def test_update_user_replaces_tracked_email_after_success() -> None:
    session = Mock()
    session.request.side_effect = [_response(201), _response(200)]
    client = UsersClient(_settings(), session=session)
    create_payload = CreateUserRequest(name="Jane", email="jane@example.com", age=30)
    update_payload = UpdateUserRequest(
        name="Jane Updated",
        email="jane.updated@example.com",
        age=31,
    )

    client.create_user(create_payload)
    client.update_user(create_payload.email, update_payload)

    assert client.tracked_user_emails() == ("jane.updated@example.com",)


def test_delete_user_removes_email_from_tracking_after_success() -> None:
    session = Mock()
    session.request.side_effect = [_response(201), _response(204)]
    client = UsersClient(_settings(), session=session)
    payload = CreateUserRequest(name="Jane", email="jane@example.com", age=30)

    client.create_user(payload)
    client.delete_user(payload.email)

    assert client.tracked_user_emails() == ()
