from fastapi import Depends
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from jose import JWTError, jwt

from app.core.config import config
from app.core.exceptions import PermissionDeniedError


security = HTTPBearer()


async def get_access_token(
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    ),
) -> str:

    return credentials.credentials


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    ),
) -> dict:

    token = credentials.credentials

    try:

        payload = jwt.decode(
            token,
            config.SECRET_KEY,
            algorithms=[config.ALGORITHM],
        )

    except JWTError:

        raise PermissionDeniedError(
            "Invalid or expired access token"
        )

    user_id = payload.get("sub")
    role = payload.get("role")

    if not user_id:

        raise PermissionDeniedError(
            "Invalid access token"
        )

    return {
        "user_id": user_id,
        "role": role,
    }


async def require_admin(
    current_user: dict = Depends(
        get_current_user
    ),
) -> dict:

    if current_user["role"] != "admin":

        raise PermissionDeniedError(
            "Admin access required"
        )

    return current_user


async def require_restaurant_owner(
    current_user: dict = Depends(
        get_current_user
    ),
) -> dict:

    if current_user["role"] != "restaurant_owner":

        raise PermissionDeniedError(
            "Restaurant owner access required"
        )

    return current_user