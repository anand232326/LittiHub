
from typing import Any

from app.core.config import config
from app.core.exceptions import (
    AuthenticationError,
    InvalidRequestError,
    PermissionDeniedError,
    ResourceNotFoundError,
    ServiceCommunicationError,
)
from app.core.http_client import http_client


class UserClient:

    def __init__(self) -> None:
        self.base_url = config.USER_SERVICE_URL.rstrip("/")

    async def create_profile(
        self,
        data: dict[str, Any],
        token: str,
    ) -> dict[str, Any]:
        response = await http_client.request(
            method="POST",
            url=f"{self.base_url}/api/v1/users/profile",
            json=data,
            headers={
                "Authorization": token,
            },
        )

        return self._handle_response(response)

    async def get_my_profile(
        self,
        token: str,
    ) -> dict[str, Any]:
        response = await http_client.request(
            method="GET",
            url=f"{self.base_url}/api/v1/users/me",
            headers={
                "Authorization": token,
            },
        )

        return self._handle_response(response)

    async def update_my_profile(
        self,
        data: dict[str, Any],
        token: str,
    ) -> dict[str, Any]:
        response = await http_client.request(
            method="PATCH",
            url=f"{self.base_url}/api/v1/users/me",
            json=data,
            headers={
                "Authorization": token,
            },
        )

        return self._handle_response(response)

    def _handle_response(
        self,
        response,
    ) -> dict[str, Any]:

        if response.status_code in (400, 422):
            raise InvalidRequestError(
                self._get_error_message(
                    response,
                    "Invalid user request",
                )
            )

        if response.status_code == 401:
            raise AuthenticationError(
                self._get_error_message(
                    response,
                    "Authentication failed",
                )
            )

        if response.status_code == 403:
            raise PermissionDeniedError(
                self._get_error_message(
                    response,
                    "Permission denied",
                )
            )

        if response.status_code == 404:
            raise ResourceNotFoundError(
                self._get_error_message(
                    response,
                    "User profile not found",
                )
            )

        if response.status_code >= 500:
            raise ServiceCommunicationError(
                "User service is unavailable"
            )

        if response.status_code >= 400:
            raise ServiceCommunicationError(
                "User service request failed"
            )

        try:
            data = response.json()

        except ValueError as exc:
            raise ServiceCommunicationError(
                "Invalid response from user service"
            ) from exc

        if not isinstance(data, dict):
            raise ServiceCommunicationError(
                "Unexpected response format from user service"
            )

        return data

    @staticmethod
    def _get_error_message(
        response,
        default: str,
    ) -> str:
        try:
            data = response.json()

            if isinstance(data, dict):
                message = data.get("message")

                if isinstance(message, str) and message.strip():
                    return message

        except ValueError:
            pass

        return default


user_client = UserClient()
