
from pymongo import AsyncMongoClient
from beanie import init_beanie

from app.core.config import Config
from app.models.restaurant import Restaurant


client = AsyncMongoClient(Config.MONGO_URL)

database = client[Config.MONGO_DB]


async def init_db():
    await init_beanie(
        database=database,
        document_models=[Restaurant],
    )


async def close_db():
    await client.close()

