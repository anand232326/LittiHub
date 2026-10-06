
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.config import config
from app.core.http_client import http_client
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.restaurants import router as restaurants_router
from app.routers.cart import router as cart_router
from app.routers.orders import router as orders_router
from app.routers.inventory import router as inventory_router





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

app.include_router(auth_router)
app.include_router(restaurants_router)
app.include_router(users_router)
app.include_router(cart_router)
app.include_router(orders_router)
app.include_router(inventory_router)




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

