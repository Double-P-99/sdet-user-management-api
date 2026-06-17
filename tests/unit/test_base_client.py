"""Unit tests for the generic HTTP client."""

from __future__ import annotations

from unittest.mock import Mock

import pytest

from api.base_client import BaseClient
from config.settings import Settings


pytestmark = [pytest.mark.unit]


def _settings() -> Settings:
    return Settings(
        base_url="http://localhost:3000",
        environment="dev",
        auth_token="mysecrettoken",
        timeout=7.5,
    )


def test_build_url_uses_environment_prefix() -> None:
    client = BaseClient(_settings())

    assert client.build_url("/users/example@example.com") == (
        "http://localhost:3000/dev/users/example@example.com"
    )


def test_post_delegates_to_session_request() -> None:
    session = Mock()
    expected_response = Mock()
    session.request.return_value = expected_response
    client = BaseClient(_settings(), session=session)

    response = client.post("users", json={"name": "Jane"})

    assert response is expected_response
    session.request.assert_called_once_with(
        method="POST",
        url="http://localhost:3000/dev/users",
        headers=None,
        json={"name": "Jane"},
        params=None,
        timeout=7.5,
    )
