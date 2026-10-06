
from typing import Any

from app.core.config import config
from app.core.exceptions import (
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

    async def get_inventory(
        self,
        menu_item_id: str,
        access_token: str,
    ) -> dict[str, Any]:

        response = await http_client.request(
            method="GET",
            url=(
                f"{self.base_url}"
                f"/api/inventory/{menu_item_id}"
            ),
            headers={
                "Authorization": f"Bearer {access_token}",
            },
        )

        return await self._handle_response(response)

    async def check_stock(
        self,
        menu_item_id: str,
        quantity: int,
        access_token: str,
    ) -> dict[str, Any]:

        response = await http_client.request(
            method="POST",
            url=(
                f"{self.base_url}"
                f"/api/inventory/{menu_item_id}/check"
            ),
            headers={
                "Authorization": f"Bearer {access_token}",
            },
            json={
                "quantity": quantity,
            },
        )

        return await self._handle_response(response)

    async def reserve_stock(
        self,
        data: dict[str, Any],
        access_token: str,
    ) -> dict[str, Any]:

        response = await http_client.request(
            method="POST",
            url=f"{self.base_url}/api/inventory/reserve",
            headers={
                "Authorization": f"Bearer {access_token}",
            },
            json=data,
        )

        return await self._handle_response(response)

    async def release_stock(
        self,
        data: dict[str, Any],
        access_token: str,
    ) -> dict[str, Any]:

        response = await http_client.request(
            method="POST",
            url=f"{self.base_url}/api/inventory/release",
            headers={
                "Authorization": f"Bearer {access_token}",
            },
            json=data,
        )

        return await self._handle_response(response)

    async def update_stock(
        self,
        menu_item_id: str,
        data: dict[str, Any],
        access_token: str,
    ) -> dict[str, Any]:

        response = await http_client.request(
            method="PATCH",
            url=(
                f"{self.base_url}"
                f"/api/inventory/{menu_item_id}"
            ),
            headers={
                "Authorization": f"Bearer {access_token}",
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
