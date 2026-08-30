from pymongo import AsyncMongoClient
from beanie import init_beanie
from app.models.restaurant import Restaurant
from app.core.config import Config
from app.models.user import User


mongo_uri = (
    f"mongodb://"
    f"{Config.MONGO_USERNAME}:"
    f"{Config.MONGO_PASSWORD}@"
    f"{Config.MONGO_HOST}:"
    f"{Config.MONGO_PORT}/"
    f"?authSource=admin"
)
                           
                                                      
client = AsyncMongoClient(mongo_uri)

database = client[Config.MONGO_DATABASE]


async def init_db() -> None:

    await client.admin.command("ping")

    await init_beanie(
        database=database,
        document_models=[
            User,
            Restaurant,
        ],
    )

    print("MongoDB and Beanie initialized successfully")