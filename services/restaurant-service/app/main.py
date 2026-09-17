from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import Config
from app.core.database import close_db, init_db
from app.core.exceptions import AppException
from app.core.logger import logger
from app.middleware.error_handler import app_exception_handler
from app.middleware.logging import logging_middleware
from app.middleware.request_id import request_id_middleware
from app.routers.restaurant import router as restaurant_router


API_V1_PREFIX = "/api/v1"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()

    logger.info(
        "Restaurant Service database initialized successfully"
    )

    yield

    # Shutdown
    await close_db()

    logger.info(
        "Restaurant Service database connection closed"
    )


app = FastAPI(
    title=Config.APP_NAME,
    description="Restaurant management service for LittiHub",
    version=Config.APP_VERSION,
    lifespan=lifespan,
)


# Exception handler
app.add_exception_handler(
    AppException,
    app_exception_handler,
)


# Middleware
app.middleware("http")(request_id_middleware)
app.middleware("http")(logging_middleware)


# API routers
app.include_router(
    restaurant_router,
    prefix=API_V1_PREFIX,
)


@app.get("/")
async def root():
    return {
        "service": "restaurant-service",
        "message": "LittiHub Restaurant Service is running",
        "environment": Config.ENVIRONMENT,
    }


@app.get("/health")
async def health_check():
    return {
        "service": "restaurant-service",
        "status": "healthy",
    }