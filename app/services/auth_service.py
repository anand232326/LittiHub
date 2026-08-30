from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password,create_access_token,verify_password
from app.core.exceptions import UserAlreadyExistsError,InvalidCredentialsError
from app.schemas.auth import LoginRequest

class AuthService:

    def __init__(self):
        self.user_repository = UserRepository()

    async def register(self,email: str,full_name: str,phone: str | None,password: str, ) -> User:
        # 1. Check whether the email is already registered
        existing_user = await self.user_repository.get_by_email(
            email
        )

        if existing_user:
            raise UserAlreadyExistsError(
                "User with this email already exists"
            )

        # 2. Hash the password before storing it
        hashed_password = hash_password(password)

        # 3. Create a Beanie User document
        user = User(
            email=email,
            full_name=full_name,
            phone=phone,
            hashed_password=hashed_password,
        )

        # 4. Save the user through the repository
        user = await self.user_repository.create(user)

        # 5. Return the created user
        return user


    async def login(self,login_data:LoginRequest):
        user=await self.user_repository.get_by_email(
            login_data.email
        )
        if not user:
            raise InvalidCredentialsError(
                "Invalid email or password"
            )
        if not verify_password(
            login_data.password,
            user.hashed_password,
            ):
            raise InvalidCredentialsError("" \
            "Invalid email and password")
        
        access_token=create_access_token(
            user_id=str(user.id),
            email=str(user.email),
            role=user.role,
        )
        return access_token
    


auth_service = AuthService()