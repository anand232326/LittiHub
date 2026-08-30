from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext

from app.core.config import Config
from app.core.exceptions import InvalidTokenError

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    """Hash a raw password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a raw password against its hashed value."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: str, email: str, role: str) -> str:
    """Generate a signed JWT access token with expiration."""
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload: Dict[str, Any] = {
        "sub": user_id,
        "email": email,
        "role": role,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        Config.JWT_SECRET_KEY,
        algorithm=Config.JWT_ALGORITHM,
    )


def verify_access_token(token: str) -> Dict[str, Any]:
    """Decode and validate a JWT access token."""
    try:
        payload = jwt.decode(
            token,
            Config.JWT_SECRET_KEY,
            algorithms=[Config.JWT_ALGORITHM],
        )
        return payload
    except ExpiredSignatureError:
        raise InvalidTokenError("Token has expired")
    except JWTError:
        raise InvalidTokenError("Invalid token or signature")