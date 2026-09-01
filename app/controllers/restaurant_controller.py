from fastapi import HTTPException, status
from app.schemas.restaurant import RestaurantCreate,RestaurantResponse,PaginatedResponse,RestaurantUpdate
from app.services.restaurant_service import restaurant_service
from app.core.enums import SortOrder, RestaurantSortField


class RestaurantController:

    async def create(self,restaurant_data: RestaurantCreate,) -> RestaurantResponse:
        return await restaurant_service.create(
            restaurant_data
        )


    async def get_by_id(self,restaurant_id:str,)->RestaurantResponse:
        restaurant=await restaurant_service.get_by_id(restaurant_id)

        if restaurant is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="restaurant not found"
            )
        return restaurant


    async def get_all(self,city: str | None = None,is_active: bool | None = None,page: int = 1,
    page_size: int = 10,
    sort_by: RestaurantSortField = RestaurantSortField.CREATED_AT,
    sort_order: SortOrder = SortOrder.DESC,
    ) -> PaginatedResponse[RestaurantResponse]:

       return await restaurant_service.get_all(
        city=city,
        is_active=is_active,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order,
       )



    async def update(self,restaurant_id: str,restaurant_data: RestaurantUpdate,) -> RestaurantResponse:
        restaurant = await restaurant_service.update(
         restaurant_id,
         restaurant_data,
        )

        if restaurant is None:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Restaurant with id '{restaurant_id}' not found",
        )

        return restaurant
 


restaurant_controller = RestaurantController()