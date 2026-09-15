from beanie import init_beanie
from pymongo import AsyncMongoClient

from app.core.config import settings
from app.models.user import User

# Instantiate PyMongo's async client
client = AsyncMongoClient(settings.MONGO_URL)
database = client[settings.MONGO_DB]


async def init_db():
    await init_beanie(
        database=database,
        document_models=[
            User,
        ],
    )


async def close_db():
    await client.close()