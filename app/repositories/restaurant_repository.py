from app.models.restaurant import Restaurant
from bson import ObjectId
from bson.errors import InvalidId

class RestaurantRepository:

    async def create(self,restaurant: Restaurant,) -> Restaurant:
        await restaurant.insert()
        return restaurant


    async def get_by_id(self,restaurant_id:str,)->Restaurant|None:
        try:
            object_id = ObjectId(restaurant_id)
        except InvalidId:
            return None

        return await Restaurant.get(object_id) 



    async def get_all(self,city:str |None=None,)->list[Restaurant]:
        query={}
        if city:
            query["city"]=city

        return await Restaurant.find(query).to_list()      


restaurant_repository = RestaurantRepository()