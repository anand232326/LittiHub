
import httpx

from app.core.config import config
from app.core.exceptions import (
    ExternalServiceError,
    ResourceNotFoundError,
)


class MenuClient:

    def __init__(self):
        self.base_url = (
            config.MENU_SERVICE_URL.rstrip("/")
        )

    async def get_menu_item(
        self,
        restaurant_id: str,
        item_id: str,
        access_token: str,
    ) -> dict:

        url = (
            f"{self.base_url}"
            f"/api/v1/restaurants/"
            f"{restaurant_id}/menu/items/"
            f"{item_id}"
        )

        headers = {
            "Authorization": (
                f"Bearer {access_token}"
            )
        }

        try:

            async with httpx.AsyncClient(
                timeout=5.0
            ) as client:

                response = await client.get(
                    url,
                    headers=headers,
                )

        except httpx.RequestError as exc:

            raise ExternalServiceError(
                "Menu service is unavailable"
            ) from exc

        if response.status_code == 404:

            raise ResourceNotFoundError(
                "Menu item not found"
            )

        if response.status_code >= 500:

            raise ExternalServiceError(
                "Menu service failed"
            )

        if response.status_code >= 400:

            raise ExternalServiceError(
                "Unable to retrieve menu item"
            )

        return response.json()


menu_client = MenuClient()

