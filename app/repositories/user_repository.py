from app.models.user import User
from bson import ObjectId


class UserRepository:

    async def get_by_email(self, email: str) -> User | None:
        return await User.find_one(
            {"email": email}
        )


    async def create(self, user: User) -> User:
        await user.insert()
        return user


    async def get_by_id(self,user_id:str)->User|None:
        try:
            object_id=ObjectId(user_id)

        except Exception:
            return None

        return await User.get(object_id)   


    async def update( self, user: User,) -> User:
        await user.save()
    

        return user 


user_repository = UserRepository()