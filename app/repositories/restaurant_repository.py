from app.models.restaurant import Restaurant


class RestaurantRepository:

    async def create(self,restaurant: Restaurant,) -> Restaurant:
        await restaurant.insert()
        return restaurant


restaurant_repository = RestaurantRepository()