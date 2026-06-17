"""Runtime settings for base URL, environment, and auth configuration."""

from __future__ import annotations

import os
from dataclasses import dataclass


VALID_ENVIRONMENTS = ("dev", "prod")


@dataclass(frozen=True)
class Settings:
    """Centralized runtime configuration for local runs and CI."""

    base_url: str
    environment: str
    auth_token: str
    timeout: float = 10.0

    @classmethod
    def from_env(cls) -> "Settings":
        """Build settings from environment variables with safe defaults."""
        environment = os.getenv("TEST_ENV", "dev").strip().lower()
        if environment not in VALID_ENVIRONMENTS:
            raise ValueError(
                f"Unsupported TEST_ENV '{environment}'. Expected one of {VALID_ENVIRONMENTS}."
            )

        return cls(
            base_url=os.getenv("BASE_URL", "http://localhost:3000").rstrip("/"),
            environment=environment,
            auth_token=os.getenv("AUTH_TOKEN", "mysecrettoken"),
            timeout=float(os.getenv("REQUEST_TIMEOUT", "10")),
        )


def get_settings() -> Settings:
    """Convenience accessor used by fixtures and clients."""
    return Settings.from_env()
