from fastapi import Depends
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from app.core.exceptions import AppException
from app.core.config import Config
from jose import JWTError, jwt


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

        raise AppException(
            "Invalid or expired access token",
            status_code=401,
        ) from exc

    user_id = payload.get("sub")

    if not user_id:

        raise AppException(
            "Invalid access token",
            status_code=401,
        )

    return payload