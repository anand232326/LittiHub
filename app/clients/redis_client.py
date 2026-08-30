from redis.asyncio import Redis

from app.core.config import Config


redis_client = Redis.from_url(
    Config.REDIS_URL,
    encoding="utf-8",
    decode_responses=True,
)


async def check_redis_connection() -> None:
    await redis_client.ping()


async def close_redis_connection() -> None:
    await redis_client.aclose()