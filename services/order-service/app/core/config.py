
import os
from pathlib import Path

from dotenv import load_dotenv


SERVICE_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(
    SERVICE_ROOT / ".env"
)


def get_required_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise RuntimeError(
            f"Required environment variable '{name}' is missing"
        )

    return value


class Config:

    APP_NAME = os.getenv(
        "APP_NAME",
        "LittiHub Order Service",
    )

    APP_VERSION = os.getenv(
        "APP_VERSION",
        "1.0.0",
    )

    LOG_LEVEL = os.getenv(
        "LOG_LEVEL",
        
    )

    ENVIRONMENT = os.getenv(
        "ENVIRONMENT",
        "development",
    )

    MONGO_URL = get_required_env(
        "MONGO_URL"
    )

    MONGO_DB = get_required_env(
        "MONGO_DB"
    )

    REDIS_URL = get_required_env(
        "REDIS_URL"
    )

    SECRET_KEY = get_required_env(
        "SECRET_KEY"
    )

    ALGORITHM = os.getenv(
        "ALGORITHM",
        "HS256",
    )

    USER_SERVICE_URL = get_required_env(
        "USER_SERVICE_URL"
    )

    RESTAURANT_SERVICE_URL = get_required_env(
        "RESTAURANT_SERVICE_URL"
    )

    MENU_SERVICE_URL = get_required_env(
        "MENU_SERVICE_URL"
    )

  


config = Config()

