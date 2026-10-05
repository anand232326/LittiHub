from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import Config
from app.core.database import (
    close_database,
    connect_database,
)
from app.events.producer import (
    close_kafka,
    init_kafka,
)
from app.middleware.logging import (
    logging_middleware,
)
from app.core.exceptions import AppException
from app.middleware.exception_handler import (
    app_exception_handler,
)
from app.middleware.request_id import (request_id_middleware,)
from app.routers.inventory import router as inventory_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    await connect_database()
    await init_kafka()

    yield
    await close_kafka()

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
app.middleware("http")(
    logging_middleware
)


app.include_router(
    inventory_router,
)