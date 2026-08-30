import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    APP_NAME: str = os.getenv(
        "APP_NAME",
        "LittiHub Auth Service",
    )

    APP_VERSION: str = os.getenv(
        "APP_VERSION",
        "1.0.0",
    )

    ENVIRONMENT: str = os.getenv(
        "ENVIRONMENT",
        "development",
    )

    APP_ENV: str = os.getenv(
        "APP_ENV",
        "development",
    )

    # MongoDB
    MONGO_HOST: str = os.getenv(
        "MONGO_HOST",
        "localhost",
    )

    MONGO_PORT: int = int(
        os.getenv(
            "MONGO_PORT",
            "27018",
        )
    )

    MONGO_USERNAME: str = os.getenv(
        "MONGO_USERNAME",
        "admin",
    )

    MONGO_PASSWORD: str = os.getenv(
        "MONGO_PASSWORD",
        "adminpassword",
    )

    MONGO_DATABASE: str = os.getenv(
        "MONGO_DATABASE",
        "littihub_auth",
    )

    # Redis
    REDIS_URL: str = os.getenv(
        "REDIS_URL",
        "redis://localhost:6379/0",
    )

    # JWT
    JWT_SECRET_KEY: str = os.getenv(
        "JWT_SECRET_KEY",
        "development-secret",
    )

    JWT_ALGORITHM: str = os.getenv(
        "JWT_ALGORITHM",
        "HS256",
    )

    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv(
            "ACCESS_TOKEN_EXPIRE_MINUTES",
            "30",
        )
    )


Config = Config()