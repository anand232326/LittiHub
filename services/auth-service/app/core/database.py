
from pymongo import AsyncMongoClient
from beanie import init_beanie

from app.core.config import Config
from app.models.user import User


# MongoDB async client
client = AsyncMongoClient(
    Config.MONGO_URL
)


# Auth Service database
database = client[Config.MONGO_DB]


async def init_db():
    await init_beanie(
        database=database,
        document_models=[
            User,
        ],
    )


async def close_db():
    await client.close()

