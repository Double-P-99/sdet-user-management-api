"""Reusable API response validators."""

from __future__ import annotations

from typing import Any

from requests import Response

from models.user import ErrorResponse, User


def assert_status_code(response: Response, expected_status: int) -> None:
    """Assert the response status code with a useful failure message."""
    assert response.status_code == expected_status, (
        f"Expected status {expected_status}, got {response.status_code}. "
        f"Body: {response.text}"
    )


def assert_json_content_type(response: Response) -> None:
    """Assert the response declares a JSON content type."""
    content_type = response.headers.get("content-type", "")
    assert "application/json" in content_type.lower(), (
        f"Expected JSON content type, got '{content_type}'."
    )


def assert_user_shape(payload: dict[str, Any]) -> None:
    """Assert a response body matches the documented User contract."""
    User.model_validate(payload)


def assert_error_response(response: Response) -> ErrorResponse:
    """Assert the response follows the documented ErrorResponse schema."""
    assert_json_content_type(response)
    return ErrorResponse.model_validate(response.json())
