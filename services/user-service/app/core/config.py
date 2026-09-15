import os
from pathlib import Path
from dotenv import load_dotenv

# Resolves to services/user-service/ directory
SERVICE_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(SERVICE_ROOT / ".env")


def get_required_env(name: str, default: str = None) -> str:
    value = os.getenv(name, default)
    if not value:
        raise RuntimeError(
            f"Required environment variable '{name}' is missing."
        )
    return value


class Config:
    APP_NAME: str = os.getenv("APP_NAME", "LittiHub User Service")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # Database & Cache settings
    MONGO_URL: str = get_required_env("MONGO_URL", "mongodb://localhost:27017")
    MONGO_DB: str = get_required_env("MONGO_DB", "littihub_user")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")

    # Auth & Security settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-key-change-in-prod")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    )


settings = Config()