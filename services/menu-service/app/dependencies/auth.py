from typing import Callable

from fastapi import Depends
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from jose import JWTError, jwt

from app.core.config import Config
from app.core.exceptions import (
    AuthenticationError,
    PermissionDeniedError,
)


security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    ),
) -> dict:

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            Config.SECRET_KEY,
            algorithms=[Config.ALGORITHM],
        )

    except JWTError as exc:

        raise AuthenticationError() from exc

    user_id = payload.get("sub")

    if not user_id:
        raise AuthenticationError(
            "Invalid access token"
        )

    return payload






def require_roles(
    *allowed_roles: str,
) -> Callable:

    async def role_checker(
        current_user: dict = Depends(
            get_current_user
        ),
    ) -> dict:

        user_role = current_user.get(
            "role"
        )

        if user_role not in allowed_roles:

            raise PermissionDeniedError(
                "You do not have permission to perform this action"
            )

        return current_user

    return role_checker