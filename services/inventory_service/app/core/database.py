from pymongo import AsyncMongoClient
from beanie import init_beanie
from app.core.config import Config
from app.models.inventory import Inventory


client: AsyncMongoClient | None = None


async def connect_database() -> None:
    global client

    client = AsyncMongoClient(
        Config.MONGO_URL
    )

    database = client[
        Config.MONGO_DB
    ]

    await init_beanie(
        database=database,
        document_models=[
            Inventory,
        ],
    )


async def close_database() -> None:
    global client

    if client:
        await client.close()
        client = None