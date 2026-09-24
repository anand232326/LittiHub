
from pymongo import AsyncMongoClient
from beanie import init_beanie
from app.core.config import config
from app.models.order import Order


mongo_client: AsyncMongoClient | None = None


async def connect_database() -> None:
    global mongo_client

    mongo_client = AsyncMongoClient(
        config.MONGO_URL
    )

    await mongo_client.admin.command(
        "ping"
    )

    await init_beanie(
        database=mongo_client[config.MONGO_DB],
        document_models=[
            Order,
        ],
    )


async def close_database() -> None:
    global mongo_client

    if mongo_client is not None:
        await mongo_client.close()

        mongo_client = None

