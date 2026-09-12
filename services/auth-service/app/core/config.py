
import os
from pathlib import Path

from dotenv import load_dotenv


# auth-service/
SERVICE_ROOT = Path(__file__).resolve().parents[2]

# Load this service's .env file
load_dotenv(SERVICE_ROOT / ".env")


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
        "LittiHub Auth Service",
    )

    APP_VERSION = os.getenv(
        "APP_VERSION",
        "1.0.0",
    )

    ENVIRONMENT = os.getenv(
        "ENVIRONMENT",
        "development",
    )

    MONGO_URL = get_required_env("MONGO_URL")

    MONGO_DB = get_required_env("MONGO_DB")

    SECRET_KEY = get_required_env("SECRET_KEY")

    ALGORITHM = os.getenv(
        "ALGORITHM",
        "HS256",
    )

    ACCESS_TOKEN_EXPIRE_MINUTES = int(
        os.getenv(
            "ACCESS_TOKEN_EXPIRE_MINUTES",
            "30",
        )
    )

