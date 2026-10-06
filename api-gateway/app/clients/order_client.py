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


class OrderClient:

    def __init__(self) -> None:
        self.base_url = (
            config.ORDER_SERVICE_URL.rstrip("/")
        )

    async def create_order(
        self,
        data: dict[str, Any],
        token: str,
        idempotency_key: str,
    ) -> dict[str, Any]:

        response = await http_client.request(
            method="POST",
            url=f"{self.base_url}/api/v1/orders",
            headers={
                "Authorization": token,
                "Idempotency-Key": idempotency_key,
            },
            json=data,
        )

        return await self._handle_response(response)

    async def get_orders(
        self,
        token: str,
    ) -> dict[str, Any] | list[Any]:

        response = await http_client.request(
            method="GET",
            url=f"{self.base_url}/api/v1/orders",
            headers={
                "Authorization": token,
            },
        )

        return await self._handle_response(response)

    async def get_order(
        self,
        order_id: str,
        token: str,
    ) -> dict[str, Any]:

        response = await http_client.request(
            method="GET",
            url=f"{self.base_url}/api/v1/orders/{order_id}",
            headers={
                "Authorization": token,
            },
        )

        return await self._handle_response(response)

    async def update_order_status(
        self,
        order_id: str,
        data: dict[str, Any],
        token: str,
    ) -> dict[str, Any]:

        response = await http_client.request(
            method="PATCH",
            url=(
                f"{self.base_url}"
                f"/api/v1/orders/{order_id}/status"
            ),
            headers={
                "Authorization": token,
            },
            json=data,
        )

        return await self._handle_response(response)

    async def _handle_response(
        self,
        response,
    ) -> dict[str, Any] | list[Any]:

        if response.status_code == 400:
            raise InvalidRequestError(
                self._get_error_message(
                    response,
                    "Invalid order request",
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
                    "Order not found",
                )
            )

        if response.status_code >= 500:
            raise ServiceCommunicationError(
                "Order service is unavailable"
            )

        if response.status_code >= 400:
            raise ServiceCommunicationError(
                "Order service request failed"
            )

        try:
            return response.json()

        except ValueError as exc:
            raise ServiceCommunicationError(
                "Invalid response from order service"
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


order_client = OrderClient()