from typing import Optional

from app.models.user import User


class UserRepository:

    async def create(
        self,
        user: User,
    ) -> User:

        await user.insert()

        return user

    async def get_by_auth_user_id(
        self,
        auth_user_id: str,
    ) -> Optional[User]:

        return await User.find_one(
            User.auth_user_id == auth_user_id
        )

    async def update(
        self,
        user: User,
    ) -> User:

        await user.save()

        return user