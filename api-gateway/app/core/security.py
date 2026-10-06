from dataclasses import dataclass

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.core.config import config
from app.core.exceptions import AuthenticationError


bearer_scheme = HTTPBearer(
    auto_error=False,
)


@dataclass(frozen=True)
class AuthenticatedUser:
    user_id: str
    role: str


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(
        bearer_scheme
    ),
) -> AuthenticatedUser:

    if credentials is None:
        raise AuthenticationError(
            "Authentication credentials are required"
        )

    if credentials.scheme.lower() != "bearer":
        raise AuthenticationError(
            "Invalid authentication scheme"
        )

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            config.SECRET_KEY,
            algorithms=[config.ALGORITHM],
            options={
                "require_sub": True,
                "require_exp": True,
            },
        )

    except JWTError as exc:
        raise AuthenticationError(
            "Invalid or expired authentication token"
        ) from exc

    user_id = payload.get("sub")
    role = payload.get("role")

    if not isinstance(user_id, str) or not user_id:
        raise AuthenticationError(
            "Invalid authentication token"
        )

    if not isinstance(role, str) or not role:
        raise AuthenticationError(
            "Invalid authentication token"
        )

    return AuthenticatedUser(
        user_id=user_id,
        role=role,
    )