"""Pytest fixtures for API client setup."""

from __future__ import annotations

from dataclasses import replace

import pytest

from api.users_client import UsersClient
from config.settings import Settings, get_settings


@pytest.fixture(scope="session")
def settings() -> Settings:
    """Load runtime settings once per test session."""
    return get_settings()


@pytest.fixture(scope="session")
def users_client(settings: Settings) -> UsersClient:
    """Primary API client bound to the configured environment."""
    return UsersClient(settings)


@pytest.fixture(scope="session")
def secondary_settings(settings: Settings) -> Settings:
    """Settings for the opposite environment to verify isolation behavior."""
    other_environment = "prod" if settings.environment == "dev" else "dev"
    return replace(settings, environment=other_environment)


@pytest.fixture(scope="session")
def secondary_users_client(secondary_settings: Settings) -> UsersClient:
    """Secondary API client bound to the opposite environment."""
    return UsersClient(secondary_settings)
