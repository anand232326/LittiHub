
import os
from pathlib import Path

from dotenv import load_dotenv


# auth-service/
SERVICE_ROOT = Path(__file__).resolve().parents[2]

# Load this service's .env file
load_dotenv(SERVICE_ROOT / ".env")


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

    MONGO_URL = os.getenv("MONGO_URL")

    MONGO_DB = os.getenv("MONGO_DB")

    SECRET_KEY = os.getenv("SECRET_KEY")

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

