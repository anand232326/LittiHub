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


class InventoryClient:

    def __init__(self) -> None:
        self.base_url = (
            config.INVENTORY_SERVICE_URL.rstrip("/")
        )

    async def create_inventory(
        self,
        data: dict[str, Any],
        token: str,
    ) -> dict[str, Any]:

        response = await http_client.request(
            method="POST",
            url=f"{self.base_url}/api/v1/inventory",
            headers={
                "Authorization": token,
            },
            json=data,
        )

        return await self._handle_response(response)

    async def get_inventory(
        self,
        inventory_id: str,
        token: str,
    ) -> dict[str, Any]:

        response = await http_client.request(
            method="GET",
            url=(
                f"{self.base_url}"
                f"/api/v1/inventory/{inventory_id}"
            ),
            headers={
                "Authorization": token,
            },
        )

        return await self._handle_response(response)

    async def get_inventory_by_menu_item(
        self,
        restaurant_id: str,
        menu_item_id: str,
        token: str,
    ) -> dict[str, Any]:

        response = await http_client.request(
            method="GET",
            url=(
                f"{self.base_url}"
                f"/api/v1/inventory/restaurant/"
                f"{restaurant_id}/menu-item/"
                f"{menu_item_id}"
            ),
            headers={
                "Authorization": token,
            },
        )

        return await self._handle_response(response)

    async def update_inventory(
        self,
        inventory_id: str,
        data: dict[str, Any],
        token: str,
    ) -> dict[str, Any]:

        response = await http_client.request(
            method="PATCH",
            url=(
                f"{self.base_url}"
                f"/api/v1/inventory/{inventory_id}"
            ),
            headers={
                "Authorization": token,
            },
            json=data,
        )

        return await self._handle_response(response)

    async def reserve_inventory(
        self,
        inventory_id: str,
        data: dict[str, Any],
        token: str,
    ) -> dict[str, Any]:

        response = await http_client.request(
            method="POST",
            url=(
                f"{self.base_url}"
                f"/api/v1/inventory/"
                f"{inventory_id}/reserve"
            ),
            headers={
                "Authorization": token,
            },
            json=data,
        )

        return await self._handle_response(response)

    async def release_inventory(
        self,
        inventory_id: str,
        data: dict[str, Any],
        token: str,
    ) -> dict[str, Any]:

        response = await http_client.request(
            method="POST",
            url=(
                f"{self.base_url}"
                f"/api/v1/inventory/"
                f"{inventory_id}/release"
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
    ) -> dict[str, Any]:

        if response.status_code == 400:
            raise InvalidRequestError(
                self._get_error_message(
                    response,
                    "Invalid inventory request",
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
                    "Inventory resource not found",
                )
            )

        if response.status_code >= 500:
            raise ServiceCommunicationError(
                "Inventory service is unavailable"
            )

        if response.status_code >= 400:
            raise ServiceCommunicationError(
                "Inventory service request failed"
            )

        try:
            return response.json()

        except ValueError as exc:
            raise ServiceCommunicationError(
                "Invalid response from inventory service"
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


inventory_client = InventoryClient()