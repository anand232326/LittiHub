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

        self.base_url = (
            config.USER_SERVICE_URL.rstrip("/")
        )

    async def get_user(
        self,
        user_id: str,
        token: str,
    ) -> dict[str, Any]:

        response = await http_client.request(
            method="GET",
            url=f"{self.base_url}/api/v1/users/{user_id}",
            headers={
                "Authorization": token,
            },
        )

        return await self._handle_response(
            response
        )

    async def _handle_response(
        self,
        response,
    ) -> dict[str, Any]:

        if response.status_code == 400:

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
                    "User not found",
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

            return response.json()

        except ValueError as exc:

            raise ServiceCommunicationError(
                "Invalid response from user service"
            ) from exc

    @staticmethod
    def _get_error_message(
        response,
        default: str,
    ) -> str:

        try:

            data = response.json()

            if isinstance(data, dict):

                return data.get(
                    "message",
                    default,
                )

        except ValueError:
            pass

        return default


user_client = UserClient()