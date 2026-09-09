
from fastapi import HTTPException, status

from app.schemas.restaurant_menu import (
    RestaurantMenuResponse,
)
from app.services.restaurant_menu_service import (
    restaurant_menu_service,
)


class RestaurantMenuController:

    async def get_restaurant_menu(
        self,
        restaurant_id: str,
    ) -> RestaurantMenuResponse:

        menu = await (
            restaurant_menu_service.get_restaurant_menu(
                restaurant_id
            )
        )

        if menu is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found or inactive",
            )

        return menu


restaurant_menu_controller = RestaurantMenuController()

