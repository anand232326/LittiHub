
from app.core.exceptions import (
    AuthenticationError,
    ResourceAlreadyExistsError,
    ResourceNotFoundError,
)
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.core.enums import UserRole
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    UserResponse,
)


class AuthService:
    """
    Contains authentication business logic.
    """

    def __init__(
        self,
        user_repository: UserRepository,
    ):
        self.user_repository = user_repository

    async def register(
        self,
        request: RegisterRequest,
    ) -> UserResponse:
        """
        Register a new user.
        """

        # 1. Check whether email is already registered
        existing_user = await self.user_repository.get_by_email(
            request.email
        )

        if existing_user:
            raise ResourceAlreadyExistsError(
                "Email is already registered"
            )

        # 2. Create user document
        user = User(
            email=request.email,
            password_hash=hash_password(request.password),
            first_name=request.first_name,
            last_name=request.last_name,
            role=UserRole.CUSTOMER,
        )

        # 3. Save user
        created_user = await self.user_repository.create(user)

        # 4. Convert database model → API response
        return UserResponse(
            id=str(created_user.id),
            email=created_user.email,
            first_name=created_user.first_name,
            last_name=created_user.last_name,
            role=created_user.role,
            is_active=created_user.is_active,
            is_verified=created_user.is_verified,
            created_at=created_user.created_at,
        )

    async def login(
        self,
        request: LoginRequest,
    ) -> LoginResponse:
        """
        Authenticate user and generate JWT access token.
        """

        # 1. Find user
        user = await self.user_repository.get_by_email(
            request.email
        )

        if not user:
            raise AuthenticationError()

        # 2. Check account status
        if not user.is_active:
            raise AuthenticationError(
                "User account is inactive"
            )

        # 3. Verify password
        if not verify_password(
            request.password,
            user.password_hash,
        ):
            raise AuthenticationError()

        # 4. Create JWT payload
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role.value,
        }

        # 5. Generate JWT
        access_token = create_access_token(token_data)

        # 6. Build response
        user_response = UserResponse(
            id=str(user.id),
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            role=user.role,
            is_active=user.is_active,
            is_verified=user.is_verified,
            created_at=user.created_at,
        )

        return LoginResponse(
            access_token=access_token,
            user=user_response,
        )

    async def get_user_by_id(
        self,
        user_id: str,
    ) -> UserResponse:
        """
        Get a user by ID.
        """

        user = await self.user_repository.get_by_id(user_id)

        if not user:
            raise ResourceNotFoundError(
                "User not found"
            )

        return UserResponse(
            id=str(user.id),
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            role=user.role,
            is_active=user.is_active,
            is_verified=user.is_verified,
            created_at=user.created_at,
        )

