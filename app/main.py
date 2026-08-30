from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.clients.redis_client import check_redis_connection, close_redis_connection
from app.core.config import Config
from app.core.database import init_db
from app.core.exceptions import AppException
from app.core.logger import logger
from app.middleware.error_handler import app_exception_handler
from app.middleware.logging import logging_middleware
from app.middleware.request_id import request_id_middleware
from app.routers.v1.auth import router as auth_router
from app.routers.v1.users import router as users_router
from app.routers.v1.restaurants import router as restaurant_router

API_V1_PREFIX = "/api/v1"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Application startup
    await init_db()
    await check_redis_connection()
    logger.info("Database & Redis initialized successfully")

    yield

    # Application shutdown
    await close_redis_connection()
    logger.info("Redis connection closed")
    logger.info("LittiHub API shutting down...")


app = FastAPI(
    title=Config.APP_NAME,
    description="Scalable food ordering platform",
    version=Config.APP_VERSION,
    lifespan=lifespan,
)

# Custom Exception Handlers
app.add_exception_handler(AppException, app_exception_handler)

# Middleware
app.middleware("http")(request_id_middleware)
app.middleware("http")(logging_middleware)

# Routers
app.include_router(auth_router,prefix=API_V1_PREFIX,)
app.include_router(users_router,prefix=API_V1_PREFIX,)
app.include_router(restaurant_router,prefix=API_V1_PREFIX,)


@app.get("/")
async def root():
    return {
        "message": "Welcome to LittiHub API",
        "environment": Config.ENVIRONMENT,
    }