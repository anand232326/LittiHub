
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import config
from app.core.database import (
    close_database,
    connect_database,
)
from app.core.exceptions import AppException
from app.middleware.error_handler import (
    app_exception_handler,
    generic_exception_handler,
)
from app.middleware.logging import (
    LoggingMiddleware,
)
from app.middleware.request_id import (
    RequestIDMiddleware,
)
from app.routers.order import router as order_router


@asynccontextmanager
async def lifespan(
    app: FastAPI,
):
    # Startup
    await connect_database()

    yield

    # Shutdown
    await close_database()


app = FastAPI(
    title=config.APP_NAME,
    version=config.APP_VERSION,
    lifespan=lifespan,
)


# --------------------------------------------------
# Exception handlers
# --------------------------------------------------

app.add_exception_handler(
    AppException,
    app_exception_handler,
)

app.add_exception_handler(
    Exception,
    generic_exception_handler,
)


# --------------------------------------------------
# Middleware
# --------------------------------------------------

app.add_middleware(
    RequestIDMiddleware
)

app.add_middleware(
    LoggingMiddleware
)




app.include_router(
    order_router
)


@app.get(
    "/health",
    tags=["Health"],
)
async def health_check():
    return {
        "status": "ok",
        "service": config.APP_NAME,
    }

