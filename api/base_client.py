"""Base HTTP client abstractions for the API test framework."""

from __future__ import annotations

from typing import Any
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter
from requests import Response, Session
from urllib3.util.retry import Retry

from config.settings import Settings


class BaseClient:
    """Generic HTTP client bound to a single configured environment."""

    def __init__(self, settings: Settings, session: Session | None = None) -> None:
        self.settings = settings
        self.session = session or self._build_session()

    @property
    def base_url(self) -> str:
        return self.settings.base_url

    @property
    def environment(self) -> str:
        return self.settings.environment

    def build_url(self, path: str) -> str:
        """Build a full URL under the configured environment prefix."""
        normalized_path = path.lstrip("/")
        return urljoin(f"{self.base_url}/", f"{self.environment}/{normalized_path}")

    def _build_session(self) -> Session:
        """Create a session with conservative retries for transient read requests."""
        session = requests.Session()
        retry_strategy = Retry(
            total=self.settings.request_retries,
            backoff_factor=0.25,
            status_forcelist=(502, 503, 504),
            allowed_methods=frozenset({"GET"}),
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def _request(
        self,
        method: str,
        path: str,
        *,
        headers: dict[str, str] | None = None,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Response:
        """Send an HTTP request using the shared session."""
        return self.session.request(
            method=method,
            url=self.build_url(path),
            headers=headers,
            json=json,
            params=params,
            timeout=self.settings.timeout,
        )

    def get(
        self,
        path: str,
        *,
        headers: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Response:
        return self._request(
            "GET",
            path,
            headers=headers,
            params=params,
        )

    def post(
        self,
        path: str,
        *,
        headers: dict[str, str] | None = None,
        json: dict[str, Any] | None = None,
    ) -> Response:
        return self._request(
            "POST",
            path,
            headers=headers,
            json=json,
        )

    def put(
        self,
        path: str,
        *,
        headers: dict[str, str] | None = None,
        json: dict[str, Any] | None = None,
    ) -> Response:
        return self._request(
            "PUT",
            path,
            headers=headers,
            json=json,
        )

    def delete(
        self,
        path: str,
        *,
        headers: dict[str, str] | None = None,
    ) -> Response:
        return self._request(
            "DELETE",
            path,
            headers=headers,
        )
