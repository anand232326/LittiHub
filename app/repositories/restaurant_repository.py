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



    async def get_all(self,city:str |None=None,page:int=1,page_size:int=10,)->tuple[list[Restaurant],int]:
        query={}
        if city:
            query["city"]=city

        total=await Restaurant.find(query).count()
        skip=(page-1)*page_size

        restaurants = await (
        Restaurant.find(query)
        .skip(skip)
        .limit(page_size)
        .to_list()
        )

        return restaurants,total   


restaurant_repository = RestaurantRepository()