from app.models.restaurant import Restaurant
from bson import ObjectId
from bson.errors import InvalidId
from beanie import SortDirection
from app.core.enums import SortOrder, RestaurantSortField

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



    async def get_all(self,city:str |None=None,page:int=1,page_size:int=10, is_active:bool |None=None,
                      sorted_by:RestaurantSortField=RestaurantSortField.CREATED_AT,
                      sorted_order:SortOrder=SortOrder.DESC)->tuple[list[Restaurant],int]:
        query={}
        if city:
            query["city"]=city

        if is_active is not None:
            query["is_active"]=is_active    

        total=await Restaurant.find(query).count()
        skip=(page-1)*page_size

        sort_direction = (
        SortDirection.ASCENDING
        if SortOrder == SortOrder.ASC
        else SortDirection.DESCENDING
        )

        restaurants = await (
        Restaurant.find(query)
        .skip(skip)
        .limit(page_size)
        .to_list()
        )

        return restaurants,total  


    async def update(self,restaurant:Restaurant,update_data:dict,)->Restaurant:
        await restaurant.set(update_data)

        return restaurant 


restaurant_repository = RestaurantRepository()