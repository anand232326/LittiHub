# services/order-service/app/clients/menu_client.py

import httpx

from app.core.config import config


class MenuClient:

    async def get_menu_item(
        self,
        restaurant_id: str,
        item_id: str,
    ) -> dict | None:

        url = (
            f"{config.MENU_SERVICE_URL}"
            f"/api/v1/restaurants/{restaurant_id}"
            f"/items/{item_id}"
        )

        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url)

        if response.status_code == 404:
            return None

        response.raise_for_status()

        return response.json()


menu_client = MenuClient()