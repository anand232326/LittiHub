
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.core.config import Config
from app.core.exceptions import AppException


security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:

    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            Config.SECRET_KEY,
            algorithms=[Config.ALGORITHM],
        )

    except JWTError as exc:
        print("JWT DECODE ERROR:", repr(exc))
        print("JWT SECRET LENGTH:", len(Config.SECRET_KEY))
        print("JWT ALGORITHM:", Config.ALGORITHM)

        raise AppException(
            "Invalid or expired access token",
            status_code=401,
        ) from exc

    print("JWT PAYLOAD:", payload)

    user_id = payload.get("sub")

    if not user_id:
        print("JWT ERROR: 'sub' is missing")

        raise AppException(
            "Invalid access token: subject missing",
            status_code=401,
        )

    return payload

