import httpx
from app.core.config import Config


class RestaurantClient:
    async def get_restaurant(self, restaurant_id: str, token: str = None) -> dict | None:
        url = (
            f"{Config.RESTAURANT_SERVICE_URL}"
            f"/api/v1/restaurants/{restaurant_id}"
        )

        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url, headers=headers)

        if response.status_code == 404:  # Note: 404 is standard for "not found", ensure you handle 404 instead of 400 if intended
            return None

        response.raise_for_status()

        return response.json()


restaurant_client = RestaurantClient()