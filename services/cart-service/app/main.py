from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import Config
from app.core.database import (
    check_redis_connection,
    close_redis_connection,
)
from app.core.logger import logger
from app.routers.cart import router as cart_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info(
        "Starting LittiHub Cart Service"
    )

    redis_available = await check_redis_connection()

    if not redis_available:
        logger.error(
            "Redis connection failed"
        )

    else:
        logger.info(
            "Redis connection successful"
        )

    yield

    await close_redis_connection()

    logger.info(
        "Cart Service stopped"
    )


app = FastAPI(
    title=Config.APP_NAME,
    version=Config.APP_VERSION,
    lifespan=lifespan,
)


app.include_router(
    cart_router
)


@app.get(
    "/health",
    tags=["Health"],
)
async def health_check():

    return {
        "status": "ok",
        "service": Config.APP_NAME,
    }