
import os
from pathlib import Path

from dotenv import load_dotenv


SERVICE_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(
    SERVICE_ROOT / ".env"
)


def get_required_env(
    name: str,
) -> str:

    value = os.getenv(name)

    if not value:
        raise RuntimeError(
            f"Required environment variable "
            f"'{name}' is missing"
        )

    return value


class Config:

    APP_NAME = os.getenv(
        "APP_NAME",
        "LittiHub API Gateway",
    )

    APP_VERSION = os.getenv(
        "APP_VERSION",
        "1.0.0",
    )

    ENVIRONMENT = os.getenv(
        "ENVIRONMENT",
        "development",
    )

    SECRET_KEY = get_required_env(
        "SECRET_KEY"
    )

    ALGORITHM = os.getenv(
        "ALGORITHM",
        "HS256",
    )

    AUTH_SERVICE_URL = get_required_env(
        "AUTH_SERVICE_URL"
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

    CART_SERVICE_URL = get_required_env(
        "CART_SERVICE_URL"
    )

    ORDER_SERVICE_URL = get_required_env(
        "ORDER_SERVICE_URL"
    )

    INVENTORY_SERVICE_URL = get_required_env(
        "INVENTORY_SERVICE_URL"
    )


config = Config()

