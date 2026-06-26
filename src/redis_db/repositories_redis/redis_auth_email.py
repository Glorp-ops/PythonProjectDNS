from fastapi import HTTPException
from starlette import status

from src.redis_db.repositories_redis.redis_manager import redis_manager


class RepositoryAuthEmail:
    def __init__(self, manager):
        self.manager = manager
        self.redis = manager.redis

    async def set_data_auth(self, email: str, code: str):

        if await self.manager.keys("auth:code:cooldown"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Cooldown expired"
            )

        await self.manager.set(f"auth:code:{email}", code, ex=300)
        await self.manager.set("auth:code:cooldown", "30", ex=30)
        await self.manager.set(f"auth:{email}:attempts:", "0", ex=300)

    async def mget(self, values: list[str]):
        return await self.manager.redis.mget(values)

    async def incr(self, key: str, amount: int = 1):
        await self.manager.redis.incr(key, amount)


repo_auth_email = RepositoryAuthEmail(redis_manager)
