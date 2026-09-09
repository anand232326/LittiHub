
from app.repositories.menu_category_repository import (
    menu_category_repository,
)
from app.repositories.menu_item_repository import (
    menu_item_repository,
)
from app.repositories.restaurant_repository import (
    restaurant_repository,
)
from app.schemas.restaurant_menu import (
    RestaurantMenuCategoryResponse,
    RestaurantMenuItemResponse,
    RestaurantMenuResponse,
    RestaurantMenuRestaurantResponse,
)


class RestaurantMenuService:

    def __init__(self):
        self.restaurant_repository = restaurant_repository
        self.menu_category_repository = menu_category_repository
        self.menu_item_repository = menu_item_repository


    async def get_restaurant_menu(
        self,
        restaurant_id: str,
    ) -> RestaurantMenuResponse | None:

        restaurant = await (
            self.restaurant_repository.get_by_id(
                restaurant_id
            )
        )

        if restaurant is None:
            return None

        if not restaurant.is_active:
            return None

        categories = await (
            self.menu_category_repository
            .get_active_by_restaurant(
                restaurant_id
            )
        )

        menu_items = await (
            self.menu_item_repository
            .get_active_by_restaurant(
                restaurant_id
            )
        )

        items_by_category: dict[str, list] = {}

        for item in menu_items:
            if item.category_id not in items_by_category:
                items_by_category[item.category_id] = []

            items_by_category[item.category_id].append(item)

        category_responses = []

        for category in categories:

            category_items = items_by_category.get(
                str(category.id),
                [],
            )

            category_responses.append(
                RestaurantMenuCategoryResponse(
                    id=str(category.id),
                    name=category.name,
                    description=category.description,
                    items=[
                        RestaurantMenuItemResponse(
                            id=str(item.id),
                            name=item.name,
                            description=item.description,
                            price=item.price,
                            image_url=item.image_url,
                            is_available=item.is_available,
                        )
                        for item in category_items
                    ],
                )
            )

        return RestaurantMenuResponse(
            restaurant=RestaurantMenuRestaurantResponse(
                id=str(restaurant.id),
                outlet_name=restaurant.outlet_name,
                address=restaurant.address,
                city=restaurant.city,
                locality=restaurant.locality,
            ),
            categories=category_responses,
        )


restaurant_menu_service = RestaurantMenuService()

