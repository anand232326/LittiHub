from app.models.order import Order




class OrderRepository:


    async def create(self,order: Order,) -> Order:
        await order.insert()
        return order




    async def get_by_id(self,order_id: str,) -> Order | None:
        return await Order.find_one(Order.id == order_id)



    async def get_by_user(self,user_id: str,) -> list[Order]:
        return await (Order.find(Order.user_id == user_id)
        .sort(-Order.created_at)
        .to_list()
    )




    async def update(self,order: Order,) -> Order:
        await order.save()
        return order



order_repository = OrderRepository()
