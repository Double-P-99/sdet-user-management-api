"""User endpoint client helpers."""

from __future__ import annotations

from urllib.parse import quote

from requests import Response

from api.base_client import BaseClient
from models.user import CreateUserRequest, UpdateUserRequest

class UsersClient(BaseClient):
    """Resource client for `/users` endpoints."""

    USERS_PATH = "users"

    def list_users(self) -> Response:
        return self.get(self.USERS_PATH)

    def create_user(
        self,
        payload: CreateUserRequest,
    ) -> Response:
        return self.post(
            self.USERS_PATH,
            json=payload.to_dict(),
        )

    def create_user_raw(
        self,
        payload: dict[str, object],
    ) -> Response:
        """Bypass schema typing for negative and malformed payload tests."""
        return self.post(self.USERS_PATH, json=payload)

    def get_user(self, email: str) -> Response:
        return self.get(self._user_path(email))

    def update_user(
        self,
        email: str,
        payload: UpdateUserRequest,
    ) -> Response:
        return self.put(
            self._user_path(email),
            json=payload.to_dict(),
        )

    def update_user_raw(
        self,
        email: str,
        payload: dict[str, object],
    ) -> Response:
        """Bypass schema typing for negative and malformed payload tests."""
        return self.put(self._user_path(email), json=payload)

    def delete_user(
        self,
        email: str,
        *,
        auth_token: str | None = None,
    ) -> Response:
        token = self.settings.auth_token if auth_token is None else auth_token
        return self.delete(
            self._user_path(email),
            headers={"Authentication": token},
        )

    def _user_path(self, email: str) -> str:
        """URL-encode the email because it lives in the path."""
        return f"{self.USERS_PATH}/{quote(email, safe='')}"
