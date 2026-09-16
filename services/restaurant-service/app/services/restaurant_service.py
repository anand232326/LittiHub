import re
from datetime import datetime, timezone
from app.core.exceptions import (
    ResourceAlreadyExistsError,
    ResourceNotFoundError,
)
from app.models.restaurant import Restaurant
from app.repositories.restaurant_repository import RestaurantRepository
from app.schemas.restaurant import (
    CreateRestaurantRequest,
    RestaurantResponse,
    UpdateRestaurantRequest,
)


class RestaurantService:

    def __init__(self,
        restaurant_repository: RestaurantRepository,
    ):
        self.restaurant_repository = restaurant_repository

    async def create_restaurant(
        self,
        request: CreateRestaurantRequest,
    ) -> RestaurantResponse:

        # 1. Generate slug from restaurant name
        slug = self._generate_slug(request.name)

        # 2. Check whether slug already exists
        existing_restaurant = (
            await self.restaurant_repository.get_by_slug(slug)
        )

        if existing_restaurant:
            raise ResourceAlreadyExistsError(
                "Restaurant already exists"
            )

        # 3. Create database model
        restaurant = Restaurant(
            name=request.name,
            slug=slug,
            description=request.description,
            phone=request.phone,
            email=request.email,
            address=request.address,
            city=request.city,
            state=request.state,
            pincode=request.pincode,
            latitude=request.latitude,
            longitude=request.longitude,
        )

        # 4. Save through repository
        created_restaurant = (
            await self.restaurant_repository.create(restaurant)
        )

        # 5. Convert model → response DTO
        return self._to_response(created_restaurant)

    async def get_restaurant(
        self,
        restaurant_id: str,
    ) -> RestaurantResponse:

        restaurant = (
            await self.restaurant_repository.get_by_id(
                restaurant_id
            )
        )

        if not restaurant:
            raise ResourceNotFoundError(
                "Restaurant not found"
            )

        return self._to_response(restaurant)

    async def update_restaurant(
        self,
        restaurant_id: str,
        request: UpdateRestaurantRequest,
    ) -> RestaurantResponse:

        # 1. Find existing restaurant
        restaurant = (
            await self.restaurant_repository.get_by_id(
                restaurant_id
            )
        )

        if not restaurant:
            raise ResourceNotFoundError(
                "Restaurant not found"
            )

        # 2. Get only fields actually sent by client
        update_data = request.model_dump(
            exclude_unset=True
        )

        # 3. Apply changes
        for field, value in update_data.items():
            setattr(restaurant, field, value)

        # 4. Update timestamp
        restaurant.updated_at = datetime.now(timezone.utc)

        # 5. Save changes
        updated_restaurant = (
            await self.restaurant_repository.update(
                restaurant
            )
        )

        return self._to_response(updated_restaurant)

    async def delete_restaurant(
        self,
        restaurant_id: str,
    ) -> RestaurantResponse:

        # 1. Find restaurant
        restaurant = (
            await self.restaurant_repository.get_by_id(
                restaurant_id
            )
        )

        if not restaurant:
            raise ResourceNotFoundError(
                "Restaurant not found"
            )

        # 2. Soft delete
        deleted_restaurant = (
            await self.restaurant_repository.delete(
                restaurant
            )
        )

        return self._to_response(deleted_restaurant)

    @staticmethod
    def _generate_slug(name: str) -> str:

        slug = name.lower().strip()

        slug = re.sub(
            r"[^a-z0-9\s-]",
            "",
            slug,
        )

        slug = re.sub(
            r"\s+",
            "-",
            slug,
        )

        slug = re.sub(
            r"-+",
            "-",
            slug,
        )

        return slug.strip("-")

    @staticmethod
    def _to_response(
        restaurant: Restaurant,
    ) -> RestaurantResponse:

        return RestaurantResponse(
            id=str(restaurant.id),
            name=restaurant.name,
            slug=restaurant.slug,
            description=restaurant.description,
            phone=restaurant.phone,
            email=restaurant.email,
            address=restaurant.address,
            city=restaurant.city,
            state=restaurant.state,
            pincode=restaurant.pincode,
            latitude=restaurant.latitude,
            longitude=restaurant.longitude,
            is_active=restaurant.is_active,
            is_open=restaurant.is_open,
            created_at=restaurant.created_at,
            updated_at=restaurant.updated_at,
        )