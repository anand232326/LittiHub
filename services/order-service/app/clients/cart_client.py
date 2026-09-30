
import httpx

from app.core.config import config
from app.core.exceptions import (
    ExternalServiceError,
    ResourceNotFoundError,
)


class CartClient:

    def __init__(self):
        self.base_url = (
            config.CART_SERVICE_URL.rstrip("/")
        )

    async def get_cart(
        self,
        user_id: str,
        access_token: str,
    ) -> dict:

        url = (
            f"{self.base_url}"
            "/api/v1/cart/checkout"
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
                "Cart service is unavailable"
            ) from exc

        if response.status_code == 404:

            raise ResourceNotFoundError(
                "Cart not found"
            )

        if response.status_code >= 500:

            raise ExternalServiceError(
                "Cart service failed"
            )

        if response.status_code >= 400:

            raise ExternalServiceError(
                "Unable to retrieve cart"
            )

        return response.json()

    async def clear_cart(
        self,
        user_id: str,
        access_token: str,
    ) -> None:

        url = (
            f"{self.base_url}"
            "/api/v1/cart"
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

                response = await client.delete(
                    url,
                    headers=headers,
                )

        except httpx.RequestError as exc:

            raise ExternalServiceError(
                "Cart service is unavailable"
            ) from exc

        if response.status_code >= 500:

            raise ExternalServiceError(
                "Cart service failed"
            )

        if response.status_code >= 400:

            raise ExternalServiceError(
                "Unable to clear cart"
            )


cart_client = CartClient()

