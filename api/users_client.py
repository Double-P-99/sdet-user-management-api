"""User endpoint client helpers."""

from __future__ import annotations

from urllib.parse import quote

from requests import Response

from api.base_client import BaseClient
from models.user import CreateUserRequest, UpdateUserRequest

class UsersClient(BaseClient):
    """Resource client for `/users` endpoints."""

    USERS_PATH = "users"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._tracked_user_emails: set[str] = set()

    def list_users(self) -> Response:
        return self.get(self.USERS_PATH)

    def create_user(
        self,
        payload: CreateUserRequest,
    ) -> Response:
        response = self.post(
            self.USERS_PATH,
            json=payload.to_dict(),
        )
        self._track_created_email(response, payload.email)
        return response

    def create_user_raw(
        self,
        payload: dict[str, object],
    ) -> Response:
        """Bypass schema typing for negative and malformed payload tests."""
        response = self.post(self.USERS_PATH, json=payload)
        email = payload.get("email")
        if isinstance(email, str):
            self._track_created_email(response, email)
        return response

    def get_user(self, email: str) -> Response:
        return self.get(self._user_path(email))

    def update_user(
        self,
        email: str,
        payload: UpdateUserRequest,
    ) -> Response:
        response = self.put(
            self._user_path(email),
            json=payload.to_dict(),
        )
        self._track_updated_email(response, old_email=email, new_email=payload.email)
        return response

    def update_user_raw(
        self,
        email: str,
        payload: dict[str, object],
    ) -> Response:
        """Bypass schema typing for negative and malformed payload tests."""
        response = self.put(self._user_path(email), json=payload)
        new_email = payload.get("email")
        if isinstance(new_email, str):
            self._track_updated_email(response, old_email=email, new_email=new_email)
        return response

    def delete_user(
        self,
        email: str,
        *,
        auth_token: str | None = None,
    ) -> Response:
        token = self.settings.auth_token if auth_token is None else auth_token
        response = self.delete(
            self._user_path(email),
            headers={"Authentication": token},
        )
        if response.status_code == 204:
            self._tracked_user_emails.discard(email)
        return response

    def tracked_user_emails(self) -> tuple[str, ...]:
        """Expose tracked test-created users for cleanup fixtures."""
        return tuple(self._tracked_user_emails)

    def reset_tracked_users(self) -> None:
        """Clear tracked test-created users after fixture cleanup."""
        self._tracked_user_emails.clear()

    def _user_path(self, email: str) -> str:
        """URL-encode the email because it lives in the path."""
        return f"{self.USERS_PATH}/{quote(email, safe='')}"

    def _track_created_email(self, response: Response, email: str) -> None:
        if response.status_code == 201:
            self._tracked_user_emails.add(email)

    def _track_updated_email(
        self,
        response: Response,
        *,
        old_email: str,
        new_email: str,
    ) -> None:
        if response.status_code == 200:
            # Keep both candidates so cleanup still works when the API returns
            # 200 but leaves the record addressable under the original email.
            self._tracked_user_emails.add(old_email)
            self._tracked_user_emails.add(new_email)
