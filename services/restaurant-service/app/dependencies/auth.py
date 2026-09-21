from typing import Callable
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.core.config import Config
from app.core.exceptions import AppException, PermissionDeniedError

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    token = credentials.credentials

    try:
        # Wrap Config.ALGORITHM inside a list []
        algorithms = (
            [Config.ALGORITHM]
            if isinstance(Config.ALGORITHM, str)
            else Config.ALGORITHM
        )

        payload = jwt.decode(
            token,
            Config.SECRET_KEY,
            algorithms=algorithms,
        )
    except JWTError:
        raise AppException(
            "invalid or expire access token",
            status_code=401,
        )

    user_id = payload.get("sub")

    if not user_id:
        raise AppException(
            "invalid access token",
            status_code=401,
        )

    return payload


def require_role(*allowed_roles: str) -> Callable:
    async def role_checker(
        current_user: dict = Depends(get_current_user),
    ) -> dict:
        user_role = current_user.get("role")

        if user_role not in allowed_roles:
            raise PermissionDeniedError(
                "You do not have permission to perform this action"
            )

        return current_user

    return role_checker