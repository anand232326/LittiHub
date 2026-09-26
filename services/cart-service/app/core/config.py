
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
        "LittiHub Cart Service",
    )

    APP_VERSION = os.getenv(
        "APP_VERSION",
        "1.0.0",
    )

    ENVIRONMENT = os.getenv(
        "ENVIRONMENT",
        "development",
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

    MENU_SERVICE_URL = get_required_env(
        "MENU_SERVICE_URL"
    )

