
from typing import Any

from app.core.config import config
from app.core.exceptions import (
    InvalidRequestError,
    PermissionDeniedError,
    ResourceNotFoundError,
    ServiceCommunicationError,
)
from app.core.http_client import http_client


class RestaurantClient:

    def __init__(self) -> None:
        self.base_url = (
            config.RESTAURANT_SERVICE_URL.rstrip("/")
        )

    async def get_restaurant(
        self,
        restaurant_id: str,
        access_token: str,
    ) -> dict[str, Any]:

        response = await http_client.request(
            method="GET",
            url=(
                f"{self.base_url}"
                f"/api/restaurants/{restaurant_id}"
            ),
            headers={
                "Authorization": f"Bearer {access_token}",
            },
        )

        return await self._handle_response(response)

    async def get_restaurants(
        self,
        access_token: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:

        response = await http_client.request(
            method="GET",
            url=f"{self.base_url}/api/restaurants",
            headers={
                "Authorization": f"Bearer {access_token}",
            },
            params=params,
        )

        return await self._handle_response(response)

    async def create_restaurant(
        self,
        data: dict[str, Any],
        access_token: str,
    ) -> dict[str, Any]:

        response = await http_client.request(
            method="POST",
            url=f"{self.base_url}/api/restaurants",
            headers={
                "Authorization": f"Bearer {access_token}",
            },
            json=data,
        )

        return await self._handle_response(response)

    async def update_restaurant(
        self,
        restaurant_id: str,
        data: dict[str, Any],
        access_token: str,
    ) -> dict[str, Any]:

        response = await http_client.request(
            method="PATCH",
            url=(
                f"{self.base_url}"
                f"/api/restaurants/{restaurant_id}"
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
                    "Invalid restaurant request",
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
                    "Restaurant not found",
                )
            )

        if response.status_code >= 500:
            raise ServiceCommunicationError(
                "Restaurant service is unavailable"
            )

        if response.status_code >= 400:
            raise ServiceCommunicationError(
                "Restaurant service request failed"
            )

        try:
            return response.json()

        except ValueError as exc:
            raise ServiceCommunicationError(
                "Invalid response from restaurant service"
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


restaurant_client = RestaurantClient()

