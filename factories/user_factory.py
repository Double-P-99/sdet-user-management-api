"""Factories for valid and invalid user test data."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import uuid4
from models.user import CreateUserRequest, UpdateUserRequest


@dataclass(frozen=True)
class UserOverrides:
    """Optional override values used to customize generated test users."""

    name: str | None = None
    email: str | None = None
    age: int = 30


class UserFactory:
    """Generate deterministic but unique user payloads for test scenarios."""

    @staticmethod
    def _unique_suffix() -> str:
        """Generate a short unique suffix to avoid collisions across test runs."""
        return uuid4().hex[:8]

    @staticmethod
    def build_create_user(
        *,
        overrides: UserOverrides | None = None,
    ) -> CreateUserRequest:
        unique_suffix = UserFactory._unique_suffix()
        resolved = overrides or UserOverrides()
        return CreateUserRequest(
            name=resolved.name or f"Test User {unique_suffix}",
            email=resolved.email or f"test.user.{unique_suffix}@example.com",
            age=resolved.age,
        )

    @staticmethod
    def build_update_user(
        *,
        overrides: UserOverrides | None = None,
    ) -> UpdateUserRequest:
        unique_suffix = UserFactory._unique_suffix()
        resolved = overrides or UserOverrides(age=31)
        return UpdateUserRequest(
            name=resolved.name or f"Updated User {unique_suffix}",
            email=resolved.email or f"updated.user.{unique_suffix}@example.com",
            age=resolved.age,
        )

    @staticmethod
    def missing_field_payload(missing_field: str) -> dict[str, Any]:
        payload = UserFactory.build_create_user().to_dict()
        payload.pop(missing_field, None)
        return payload

    @staticmethod
    def invalid_email_payload() -> dict[str, Any]:
        payload = UserFactory.build_create_user().to_dict()
        payload["email"] = "invalid-email"
        return payload

    @staticmethod
    def invalid_age_payload(age: Any) -> dict[str, Any]:
        payload = UserFactory.build_create_user().to_dict()
        payload["age"] = age
        return payload
