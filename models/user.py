"""Domain model for User payloads."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class BaseUserPayload(BaseModel):
    """Shared schema constraints defined by the OpenAPI specification."""

    model_config = ConfigDict(extra="forbid")

    name: str
    email: EmailStr
    age: int = Field(ge=1, le=150)

    def to_dict(self) -> dict[str, object]:
        """Serialize the model into an API-ready dictionary."""
        return self.model_dump(mode="json")


class User(BaseUserPayload):
    """Represents a persisted user resource returned by the API."""


class CreateUserRequest(BaseUserPayload):
    """Schema for POST /users payloads."""


class UpdateUserRequest(BaseUserPayload):
    """Schema for PUT /users/{email} payloads."""


class ErrorResponse(BaseModel):
    """Schema for error responses returned by the API."""

    model_config = ConfigDict(extra="forbid")

    error: str
