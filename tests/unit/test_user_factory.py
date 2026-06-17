"""Unit tests for test-data factories."""

from __future__ import annotations

import pytest

from factories.user_factory import UserFactory, UserOverrides


pytestmark = [pytest.mark.unit]


def test_build_create_user_generates_unique_emails() -> None:
    first = UserFactory.build_create_user()
    second = UserFactory.build_create_user()

    assert first.email != second.email
    assert first.name != second.name


def test_build_update_user_honors_overrides() -> None:
    payload = UserFactory.build_update_user(
        overrides=UserOverrides(name="Custom Name", email="custom@example.com", age=44)
    )

    assert payload.name == "Custom Name"
    assert payload.email == "custom@example.com"
    assert payload.age == 44
