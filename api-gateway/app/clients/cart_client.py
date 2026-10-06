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


class CartClient:

    def __init__(self) -> None:
        self.base_url = (
            config.CART_SERVICE_URL.rstrip("/")
        )

    async def get_cart(
        self,
        token: str,
    ) -> dict[str, Any]:

        response = await http_client.request(
            method="GET",
            url=f"{self.base_url}/api/v1/cart",
            headers={
                "Authorization": token,
            },
        )

        return await self._handle_response(response)

    async def add_item(
        self,
        data: dict[str, Any],
        token: str,
    ) -> dict[str, Any]:

        response = await http_client.request(
            method="POST",
            url=f"{self.base_url}/api/v1/cart/items",
            headers={
                "Authorization": token,
            },
            json=data,
        )

        return await self._handle_response(response)

    async def update_item(
        self,
        menu_item_id: str,
        data: dict[str, Any],
        token: str,
    ) -> dict[str, Any]:

        response = await http_client.request(
            method="PATCH",
            url=(
                f"{self.base_url}"
                f"/api/v1/cart/items/{menu_item_id}"
            ),
            headers={
                "Authorization": token,
            },
            json=data,
        )

        return await self._handle_response(response)

    async def remove_item(
        self,
        menu_item_id: str,
        token: str,
    ) -> dict[str, Any]:

        response = await http_client.request(
            method="DELETE",
            url=(
                f"{self.base_url}"
                f"/api/v1/cart/items/{menu_item_id}"
            ),
            headers={
                "Authorization": token,
            },
        )

        return await self._handle_response(response)

    async def clear_cart(
        self,
        token: str,
    ) -> dict[str, Any]:

        response = await http_client.request(
            method="DELETE",
            url=f"{self.base_url}/api/v1/cart",
            headers={
                "Authorization": token,
            },
        )

        return await self._handle_response(response)

    async def checkout(
        self,
        token: str,
    ) -> dict[str, Any]:

        response = await http_client.request(
            method="GET",
            url=f"{self.base_url}/api/v1/cart/checkout",
            headers={
                "Authorization": token,
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
                    "Invalid cart request",
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
                    "Cart resource not found",
                )
            )

        if response.status_code >= 500:
            raise ServiceCommunicationError(
                "Cart service is unavailable"
            )

        if response.status_code >= 400:
            raise ServiceCommunicationError(
                "Cart service request failed"
            )

        try:
            return response.json()

        except ValueError as exc:
            raise ServiceCommunicationError(
                "Invalid response from cart service"
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


cart_client = CartClient()