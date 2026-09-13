
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import Config
from app.core.database import close_db, init_db
from app.core.exceptions import AppException
from app.core.logger import logger
from app.middleware.error_handler import app_exception_handler
from app.middleware.logging import logging_middleware
from app.middleware.request_id import request_id_middleware
from app.routers.auth import router as auth_router


API_V1_PREFIX = "/api/v1"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage Auth Service startup and shutdown.
    """

    # Startup
    await init_db()

    logger.info(
        "Auth Service database initialized successfully"
    )

    yield

    # Shutdown
    await close_db()

    logger.info(
        "Auth Service database connection closed"
    )


app = FastAPI(
    title=Config.APP_NAME,
    description="Authentication and authorization service for LittiHub",
    version=Config.APP_VERSION,
    lifespan=lifespan,
)


# Application exception handler
app.add_exception_handler(
    AppException,
    app_exception_handler,
)


# Middleware
app.middleware("http")(request_id_middleware)
app.middleware("http")(logging_middleware)


# API routes
app.include_router(
    auth_router,
    prefix=API_V1_PREFIX,
)


@app.get("/")
async def root():
    return {
        "service": "auth-service",
        "message": "LittiHub Auth Service is running",
        "environment": Config.ENVIRONMENT,
    }


@app.get("/health")
async def health_check():
    return {
        "service": "auth-service",
        "status": "healthy",
    }

