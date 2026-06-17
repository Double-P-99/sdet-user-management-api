"""Unit tests for reusable API validators."""

from __future__ import annotations

from unittest.mock import Mock

import pytest

from validators.api_validators import (
    assert_error_response,
    assert_json_content_type,
    assert_status_code,
)


pytestmark = [pytest.mark.unit]


def test_assert_status_code_passes_for_expected_status() -> None:
    response = Mock(status_code=200, text="")

    assert_status_code(response, 200)


def test_assert_status_code_raises_useful_message() -> None:
    response = Mock(status_code=500, text='{"error":"boom"}')

    with pytest.raises(AssertionError, match="Expected status 200, got 500"):
        assert_status_code(response, 200)


def test_assert_json_content_type_accepts_application_json() -> None:
    response = Mock(headers={"content-type": "application/json; charset=utf-8"})

    assert_json_content_type(response)


def test_assert_error_response_validates_error_schema() -> None:
    response = Mock(
        headers={"content-type": "application/json"},
        json=Mock(return_value={"error": "User not found"}),
    )

    result = assert_error_response(response)

    assert result.error == "User not found"
