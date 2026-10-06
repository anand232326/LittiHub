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


class MenuClient:

    def __init__(self) -> None:
        self.base_url = (
            config.MENU_SERVICE_URL.rstrip("/")
        )

    async def create_category(
        self,
        restaurant_id: str,
        data: dict[str, Any],
        token: str,
    ) -> dict[str, Any]:

        response = await http_client.request(
            method="POST",
            url=(
                f"{self.base_url}"
                f"/api/v1/restaurants/{restaurant_id}/categories"
            ),
            headers={
                "Authorization": token,
            },
            json=data,
        )

        return await self._handle_response(response)

    async def create_menu_item(
        self,
        restaurant_id: str,
        category_id: str,
        data: dict[str, Any],
        token: str,
    ) -> dict[str, Any]:

        response = await http_client.request(
            method="POST",
            url=(
                f"{self.base_url}"
                f"/api/v1/restaurants/{restaurant_id}"
                f"/categories/{category_id}/items"
            ),
            headers={
                "Authorization": token,
            },
            json=data,
        )

        return await self._handle_response(response)

    async def get_menu_item(
        self,
        restaurant_id: str,
        item_id: str,
        token: str,
    ) -> dict[str, Any]:

        response = await http_client.request(
            method="GET",
            url=(
                f"{self.base_url}"
                f"/api/v1/restaurants/{restaurant_id}"
                f"/items/{item_id}"
            ),
            headers={
                "Authorization": token,
            },
        )

        return await self._handle_response(response)

    async def update_menu_item(
        self,
        restaurant_id: str,
        item_id: str,
        data: dict[str, Any],
        token: str,
    ) -> dict[str, Any]:

        response = await http_client.request(
            method="PATCH",
            url=(
                f"{self.base_url}"
                f"/api/v1/restaurants/{restaurant_id}"
                f"/items/{item_id}"
            ),
            headers={
                "Authorization": token,
            },
            json=data,
        )

        return await self._handle_response(response)

    async def delete_menu_item(
        self,
        restaurant_id: str,
        item_id: str,
        token: str,
    ) -> dict[str, Any]:

        response = await http_client.request(
            method="DELETE",
            url=(
                f"{self.base_url}"
                f"/api/v1/restaurants/{restaurant_id}"
                f"/items/{item_id}"
            ),
            headers={
                "Authorization": token,
            },
        )

        return await self._handle_response(response)

    async def restore_menu_item(
        self,
        restaurant_id: str,
        item_id: str,
        token: str,
    ) -> dict[str, Any]:

        response = await http_client.request(
            method="POST",
            url=(
                f"{self.base_url}"
                f"/api/v1/restaurants/{restaurant_id}"
                f"/items/{item_id}/restore"
            ),
            headers={
                "Authorization": token,
            },
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
                    "Invalid menu request",
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
                    "Menu resource not found",
                )
            )

        if response.status_code >= 500:
            raise ServiceCommunicationError(
                "Menu service is unavailable"
            )

        if response.status_code >= 400:
            raise ServiceCommunicationError(
                "Menu service request failed"
            )

        try:
            return response.json()

        except ValueError as exc:
            raise ServiceCommunicationError(
                "Invalid response from menu service"
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


menu_client = MenuClient()