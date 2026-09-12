
from typing import Optional

from app.models.user import User


class UserRepository:
    """
    Handles database operations related to users.
    """

    async def create(self, user: User) -> User:
        """
        Create a new user in MongoDB.
        """
        await user.insert()
        return user

    async def get_by_email(
        self,
        email: str,
    ) -> Optional[User]:
        """
        Find a user by email address.
        """
        return await User.find_one(
            User.email == email
        )

    async def get_by_id(
        self,
        user_id: str,
    ) -> Optional[User]:
        """
        Find a user by MongoDB document ID.
        """
        return await User.get(user_id)

    async def update(
        self,
        user: User,
    ) -> User:
        """
        Save changes made to an existing user.
        """
        await user.save()
        return user
