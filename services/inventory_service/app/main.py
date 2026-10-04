from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import Config
from app.core.database import (
    close_database,
    connect_database,
)
from app.middleware.request_id import (request_id_middleware,)
from app.routers.inventory import router as inventory_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    await connect_database()

    yield

    await close_database()


app = FastAPI(
    title=Config.APP_NAME,
    version=Config.APP_VERSION,
    lifespan=lifespan,
)

app.middleware("http")(
    request_id_middleware
)

app.add_exception_handler(
    AppException,
    app_exception_handler,
)

app.include_router(
    inventory_router,
)