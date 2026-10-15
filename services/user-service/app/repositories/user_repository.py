from typing import Optional
from beanie import PydanticObjectId

from app.models.user import User


class UserRepository:

    async def create(self,user: User,) -> User:
        await user.insert()
        return user


    async def get_by_auth_user_id(self,auth_user_id: str,) -> Optional[User]:
        return await User.find_one(User.auth_user_id == auth_user_id)


    async def update(self,user: User,) -> User:
        await user.save()
        return user

    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Fetch a user by their database document ID."""
        if not PydanticObjectId.is_valid(user_id):
            return None
        return await User.get(PydanticObjectId(user_id))