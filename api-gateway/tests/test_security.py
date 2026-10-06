from datetime import datetime, timedelta, timezone
from app.core.exceptions import AuthenticationError
import pytest
from fastapi.security import HTTPAuthorizationCredentials
from jose import jwt

from app.core.config import config
from app.core.security import get_current_user


def create_token(
    *,
    user_id: str = "user-123",
    role: str = "customer",
    expires_delta: timedelta = timedelta(minutes=15),
) -> str:

    now = datetime.now(timezone.utc)

    payload = {
        "sub": user_id,
        "role": role,
        "iat": now,
        "exp": now + expires_delta,
    }

    return jwt.encode(
        payload,
        config.SECRET_KEY,
        algorithm=config.ALGORITHM,
    )


@pytest.mark.asyncio
async def test_valid_token():

    token = create_token(
        user_id="user-123",
        role="customer",
    )

    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials=token,
    )

    user = await get_current_user(credentials)

    assert user.user_id == "user-123"
    assert user.role == "customer"


@pytest.mark.asyncio
async def test_missing_token():

    with pytest.raises(AuthenticationError) as exc_info:
        await get_current_user(None)

    assert "credentials are required" in str(
        exc_info.value
    )


@pytest.mark.asyncio
async def test_invalid_token():

    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials="invalid.jwt.token",
    )

    with pytest.raises(Exception) as exc_info:
        await get_current_user(credentials)

    assert "Invalid or expired" in str(
        exc_info.value
    )


@pytest.mark.asyncio
async def test_expired_token():

    token = create_token(
        expires_delta=timedelta(minutes=-1),
    )

    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials=token,
    )

    with pytest.raises(AuthenticationError) as exc_info:
        await get_current_user(credentials)

    assert "Invalid or expired" in str(
        exc_info.value
    )


@pytest.mark.asyncio
async def test_role_extraction():

    token = create_token(
        user_id="admin-123",
        role="admin",
    )

    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials=token,
    )

    user = await get_current_user(credentials)

    assert user.user_id == "admin-123"
    assert user.role == "admin"