from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import Config
from app.core.database import (
    close_db,
    init_db,
)
from app.core.exceptions import AppException
from app.core.logger import logger

from app.middleware.error_handler import (
    app_exception_handler,
)
from app.middleware.logging import (
    logging_middleware,
)
from app.middleware.request_id import (
    request_id_middleware,
)

from app.routers.menu_category import (
    router as menu_category_router,
)
from app.routers.menu_item import (
    router as menu_item_router,
)


API_V1_PREFIX = "/api/v1"


@asynccontextmanager
async def lifespan(app: FastAPI):

    await init_db()

    logger.info(
        "Menu Service database initialized successfully"
    )

    yield

    await close_db()

    logger.info(
        "Menu Service database connection closed"
    )


app = FastAPI(
    title=Config.APP_NAME,
    description="Menu management service for LittiHub",
    version=Config.APP_VERSION,
    lifespan=lifespan,
)


app.add_exception_handler(
    AppException,
    app_exception_handler,
)


app.middleware("http")(
    request_id_middleware
)

app.middleware("http")(
    logging_middleware
)


app.include_router(
    menu_category_router,
    prefix=API_V1_PREFIX,
)

app.include_router(
    menu_item_router,
    prefix=API_V1_PREFIX,
)


@app.get("/")
async def root():

    return {
        "service": "menu-service",
        "message": "LittiHub Menu Service is running",
        "environment": Config.ENVIRONMENT,
    }


@app.get("/health")
async def health_check():

    return {
        "service": "menu-service",
        "status": "healthy",
    }