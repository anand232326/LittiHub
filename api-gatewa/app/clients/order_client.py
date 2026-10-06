
from typing import Any

from app.core.config import config
from app.core.exceptions import (
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
        access_token: str,
        idempotency_key: str,
    ) -> dict[str, Any]:

        response = await http_client.request(
            method="POST",
            url=f"{self.base_url}/api/orders",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Idempotency-Key": idempotency_key,
            },
            json=data,
        )

        return await self._handle_response(response)

    async def get_order(
        self,
        order_id: str,
        access_token: str,
    ) -> dict[str, Any]:

        response = await http_client.request(
            method="GET",
            url=f"{self.base_url}/api/orders/{order_id}",
            headers={
                "Authorization": f"Bearer {access_token}",
            },
        )

        return await self._handle_response(response)

    async def get_my_orders(
        self,
        access_token: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:

        response = await http_client.request(
            method="GET",
            url=f"{self.base_url}/api/orders",
            headers={
                "Authorization": f"Bearer {access_token}",
            },
            params=params,
        )

        return await self._handle_response(response)

    async def update_order(
        self,
        order_id: str,
        data: dict[str, Any],
        access_token: str,
    ) -> dict[str, Any]:

        response = await http_client.request(
            method="PATCH",
            url=f"{self.base_url}/api/orders/{order_id}",
            headers={
                "Authorization": f"Bearer {access_token}",
            },
            json=data,
        )

        return await self._handle_response(response)

    async def cancel_order(
        self,
        order_id: str,
        access_token: str,
    ) -> dict[str, Any]:

        response = await http_client.request(
            method="POST",
            url=(
                f"{self.base_url}"
                f"/api/orders/{order_id}/cancel"
            ),
            headers={
                "Authorization": f"Bearer {access_token}",
            },
        )

        return await self._handle_response(response)

    async def _handle_response(
        self,
        response,
    ) -> dict[str, Any]:

        if response.status_code == 400:
            raise InvalidRequestError(
                self._get_error_message(
                    response,
                    "Invalid order request",
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
