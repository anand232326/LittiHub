
import logging
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


logger = logging.getLogger("littihub.gateway.auth")


class AuthClient:

    def __init__(self) -> None:
        self.base_url = config.AUTH_SERVICE_URL.rstrip("/")

    async def login(
        self,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        response = await http_client.request(
            method="POST",
            url=f"{self.base_url}/api/v1/auth/login",
            json=data,
        )

        return await self._handle_response(response)

    async def register(
        self,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        response = await http_client.request(
            method="POST",
            url=f"{self.base_url}/api/v1/auth/register",
            json=data,
        )

        return await self._handle_response(response)

    async def get_me(
        self,
        token: str,
    ) -> dict[str, Any]:
        response = await http_client.request(
            method="GET",
            url=f"{self.base_url}/api/v1/auth/me",
            headers={"Authorization": token},
        )

        return await self._handle_response(response)

    async def _handle_response(
        self,
        response,
    ) -> dict[str, Any]:
        status_code = response.status_code

        if status_code >= 500:
            logger.error(
                "Auth service returned server error: status=%s",
                status_code,
            )
            raise ServiceCommunicationError(
                "Authentication service is unavailable"
            )

        if status_code == 400 or status_code == 422:
            raise InvalidRequestError(
                self._get_error_message(
                    response,
                    "Invalid authentication request",
                )
            )

        if status_code == 401:
            raise AuthenticationError(
                self._get_error_message(
                    response,
                    "Authentication failed",
                )
            )

        if status_code == 403:
            raise PermissionDeniedError(
                self._get_error_message(
                    response,
                    "Permission denied",
                )
            )

        if status_code == 404:
            raise ResourceNotFoundError(
                self._get_error_message(
                    response,
                    "Authentication resource not found",
                )
            )

        if status_code >= 400:
            raise ServiceCommunicationError(
                "Authentication service request failed"
            )

        if not response.content:
            logger.error(
                "Auth service returned an empty success response: "
                "status=%s",
                status_code,
            )
            raise ServiceCommunicationError(
                "Authentication service returned an empty response"
            )

        try:
            data = response.json()
        except ValueError as exc:
            logger.error(
                "Auth service returned invalid JSON: status=%s",
                status_code,
            )
            raise ServiceCommunicationError(
                "Invalid response from authentication service"
            ) from exc

        if not isinstance(data, dict):
            raise ServiceCommunicationError(
                "Unexpected response format from authentication service"
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
                if isinstance(message, str) and message:
                    return message
        except ValueError:
            pass

        return default


auth_client = AuthClient()
