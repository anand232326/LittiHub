
from typing import Any

from app.core.config import config
from app.core.exceptions import (
    InvalidRequestError,
    AuthenticationError,
    PermissionDeniedError,
    ResourceNotFoundError,
    ServiceCommunicationError,
)
from app.core.http_client import http_client


class AuthClient:

    def __init__(self) -> None:

        self.base_url = (
            config.AUTH_SERVICE_URL.rstrip("/")
        )

    async def login(
        self,
        data: dict[str, Any],
    ) -> dict[str, Any]:

        response = await http_client.request(
            method="POST",
            url=f"{self.base_url}/api/auth/login",
            json=data,
        )

        return await self._handle_response(
            response
        )

    async def register(
        self,
        data: dict[str, Any],
    ) -> dict[str, Any]:

        response = await http_client.request(
            method="POST",
            url=f"{self.base_url}/api/auth/register",
            json=data,
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
                    "Invalid authentication request",
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
                    "Authentication resource not found",
                )
            )

        if response.status_code >= 500:

            raise ServiceCommunicationError(
                "Authentication service is unavailable"
            )

        if response.status_code >= 400:

            raise ServiceCommunicationError(
                "Authentication service request failed"
            )

        try:
            return response.json()

        except ValueError as exc:

            raise ServiceCommunicationError(
                "Invalid response from authentication service"
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


auth_client = AuthClient()

