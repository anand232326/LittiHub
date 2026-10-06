
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.config import config
from app.core.http_client import http_client


@asynccontextmanager
async def lifespan(
    app: FastAPI,
):
    # Startup
    await http_client.start()

    yield

    # Shutdown
    await http_client.close()


app = FastAPI(
    title=config.APP_NAME,
    version=config.APP_VERSION,
    lifespan=lifespan,
)


@app.get(
    "/health",
    tags=["Health"],
)
async def health_check() -> dict:

    return {
        "status": "healthy",
        "service": config.APP_NAME,
        "version": config.APP_VERSION,
    }

