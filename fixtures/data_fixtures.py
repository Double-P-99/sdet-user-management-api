"""Pytest fixtures for test data generation."""

from __future__ import annotations

import pytest

from factories.user_factory import UserFactory
from models.user import CreateUserRequest, UpdateUserRequest


@pytest.fixture
def create_user_payload() -> CreateUserRequest:
    """Default valid create-user payload."""
    return UserFactory.build_create_user()


@pytest.fixture
def update_user_payload() -> UpdateUserRequest:
    """Default valid update-user payload."""
    return UserFactory.build_update_user()
