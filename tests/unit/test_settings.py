"""Unit tests for runtime settings parsing."""

from __future__ import annotations

import pytest

from config.settings import Settings


pytestmark = [pytest.mark.unit]


def test_from_env_uses_documented_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("BASE_URL", raising=False)
    monkeypatch.delenv("TEST_ENV", raising=False)
    monkeypatch.delenv("AUTH_TOKEN", raising=False)
    monkeypatch.delenv("REQUEST_TIMEOUT", raising=False)

    settings = Settings.from_env()

    assert settings.base_url == "http://localhost:3000"
    assert settings.environment == "dev"
    assert settings.auth_token == "mysecrettoken"
    assert settings.timeout == 10.0


def test_from_env_normalizes_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TEST_ENV", " PROD ")

    settings = Settings.from_env()

    assert settings.environment == "prod"


def test_from_env_rejects_invalid_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TEST_ENV", "qa")

    with pytest.raises(ValueError, match="Unsupported TEST_ENV"):
        Settings.from_env()
