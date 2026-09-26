
import redis.asyncio as redis

from app.core.config import Config


redis_client = redis.from_url(
    Config.REDIS_URL,
    decode_responses=True,
)


async def check_redis_connection() -> bool:

    try:
        await redis_client.ping()
        return True

    except Exception:
        return False


async def close_redis_connection() -> None:

    await redis_client.aclose()

