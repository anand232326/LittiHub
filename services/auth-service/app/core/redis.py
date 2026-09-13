
from redis.asyncio import Redis

from app.core.config import Config


redis_client = Redis.from_url(
    Config.REDIS_URL,
    decode_responses=True,
)


async def close_redis():
    await redis_client.aclose()

