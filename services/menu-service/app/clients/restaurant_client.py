import httpx
from app.core.config import Config


class RestaurantClient:

    async def get_restaurant(self,restaurant_id:str,)->dict | None:

        url=(
            f"{Config.RESTAURANT_SERVICE_URL}"
            f"/api/v1/restaurants/{restaurant_id}"

        )

        async with httpx.AsyncClient(timeout=5.0) as client:
            response=await client.get(url)

        if response.status_code==400:
            return None

        response.raise_for_status()

        return response.json()



restaurant_client=RestaurantClient()

            