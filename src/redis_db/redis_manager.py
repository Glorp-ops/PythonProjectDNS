from typing import Any

import redis.asyncio as redis

from ..core import settings


class RedisManager:
    def __init__(
        self, port: int = settings.REDIS_PORT, host: str = settings.REDIS_HOST
    ) -> None:
        self.port = port
        self.host = host
        self.redis = None

    async def connect(self):
        self.redis = await redis.Redis(host=self.host, port=self.port, decode_responses=True)

    async def set(self, key: str, value: str, ex: int) -> None:
        await self.redis.set(key, value, ex)

    async def get(self, key: str):

        return await self.redis.get(key)

    async def keys(self, pattern: str = "*") -> Any:

        return await self.redis.keys(pattern)

    async def delete(self, key: str):
        await self.redis.unlink(key)

    async def close(self):
        await self.redis.aclose()


redis_manager = RedisManager()
