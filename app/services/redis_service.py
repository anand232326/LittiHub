import json
from app.clients.redis_client import redis_client


class RedisService:

    async def set(self,key: str,value: str,expire: int | None = None,) -> None:
        await redis_client.set(key,value,ex=expire,)

    async def get(self, key: str) -> str | None:
        return await redis_client.get(key)

    async def delete(self, key: str) -> None:
        await redis_client.delete(key)



    async def exists(self, key: str) -> bool:

        return bool(
            await redis_client.exists(key)
        )


    async def set_json( self, key: str, value: dict, expire: int | None = None,) -> None:
        serialized_value = json.dumps(value)
        await self.set(key=key,value=serialized_value,expire=expire,)


    async def get_json(self,key: str,) -> dict | None:
        value = await self.get(key)

        if value is None:
            return None

        return json.loads(value)

    async def delete_key(self, key: str) -> None:

        await self.delete(key)


redis_service = RedisService()