
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.exceptions import AuthenticationError
from app.core.security import decode_access_token


# Reads the Authorization: Bearer <token> header
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """
    Extract and validate the JWT access token.
    """

    token = credentials.credentials

    try:
        payload = decode_access_token(token)

    except ValueError as exc:
        raise AuthenticationError(
            "Invalid or expired access token"
        ) from exc

    user_id = payload.get("sub")

    if not user_id:
        raise AuthenticationError(
            "Invalid access token"
        )

    return payload

