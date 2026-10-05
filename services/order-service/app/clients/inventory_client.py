import httpx
from app.core.config import config
from app.core.exceptions import (
    ServiceCommunicationError,
)


class InventoryClient:

    def __init__(self):
        self.base_url = config.INVENTORY_SERVICE_URL

    async def reserve_inventory(
        self,
        inventory_id: str,
        quantity: int,
        access_token: str,
    ) -> dict:

        url = (
            f"{self.base_url}"
            f"/api/v1/inventory/{inventory_id}/reserve"
        )

        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        payload = {
            "quantity": quantity,
        }

        try:

            async with httpx.AsyncClient() as client:

                response = await client.post(
                    url,
                    json=payload,
                    headers=headers,
                    timeout=10.0,
                )

        except httpx.RequestError as exc:

            raise ServiceCommunicationError(
                "Unable to communicate with Inventory Service"
            ) from exc

        if response.status_code >= 400:

            raise ServiceCommunicationError(
                "Inventory Service rejected the request"
            )

        return response.json()

    async def release_inventory(
        self,
        inventory_id: str,
        quantity: int,
        access_token: str,
    ) -> dict:

        url = (
            f"{self.base_url}"
            f"/api/v1/inventory/{inventory_id}/release"
        )

        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        payload = {
            "quantity": quantity,
        }

        try:

            async with httpx.AsyncClient() as client:

                response = await client.post(
                    url,
                    json=payload,
                    headers=headers,
                    timeout=10.0,
                )

        except httpx.RequestError as exc:

            raise ServiceCommunicationError(
                "Unable to communicate with Inventory Service"
            ) from exc

        if response.status_code >= 400:

            raise ServiceCommunicationError(
                "Inventory Service rejected the request"
            )

        return response.json()


inventory_client = InventoryClient()