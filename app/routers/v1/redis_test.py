from fastapi import APIRouter

from app.services.redis_service import redis_service


router = APIRouter(
    prefix="/redis-test",
    tags=["Redis"],
)


@router.post("/")
async def test_redis():

    await redis_service.set(
        key="test:user",
        value="Anand",
        expire=60,
    )

    value = await redis_service.get("test:user")

    return {
        "key": "test:user",
        "value": value,
    }