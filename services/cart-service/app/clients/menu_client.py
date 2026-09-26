
import httpx

from app.core.config import Config
from app.core.exceptions import (
    ResourceNotFoundError,
    ServiceCommunicationError,
)


class MenuClient:

    def __init__(self):
        self.base_url = Config.MENU_SERVICE_URL

    async def get_menu_item(
        self,
        restaurant_id: str,
        item_id: str,
    ) -> dict:

        url = (
            f"{self.base_url}"
            f"/api/v1/restaurants/"
            f"{restaurant_id}/menu-items/"
            f"{item_id}"
        )

        try:

            async with httpx.AsyncClient(
                timeout=5.0
            ) as client:

                response = await client.get(
                    url
                )

        except httpx.RequestError as exc:

            raise ServiceCommunicationError(
                "Unable to communicate with "
                "Menu Service"
            ) from exc

        if response.status_code == 404:

            raise ResourceNotFoundError(
                "Menu item not found"
            )

        if response.status_code >= 500:

            raise ServiceCommunicationError(
                "Menu Service is unavailable"
            )

        if response.status_code >= 400:

            raise ServiceCommunicationError(
                "Menu Service request failed"
            )

        return response.json()


menu_client = MenuClient()

