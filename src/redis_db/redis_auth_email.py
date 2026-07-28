from fastapi import HTTPException
from starlette import status

from .redis_manager import redis_manager


class RepositoryAuthEmail:
    def __init__(self, manager) -> None:
        self.manager = manager
        self.redis = manager.redis

    async def set_data_auth(
        self,
        code: str,
        secret: str,
        email: str | None = None,
        password: str | None = None,
    ):

        if await self.manager.keys(f"auth:code:{email}:cooldown"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Cooldown expired"
            )
        await self.manager.set(key=f"auth:code:{email}", value=code, ex=300)

        if email is not None:
            await self.manager.set(key=f"auth:{secret}", value=email, ex=300)

        await self.manager.set(key=f"auth:code:{email}:cooldown", value="30", ex=30)
        await self.manager.set(key=f"auth:{email}:attempts", value="5", ex=300)

        if password:
            await self.manager.set(key=f"auth:password:{email}", value=password, ex=300)

    async def delete_auth_data(self, secret: str, email: str, password: bool = False):

        await self.manager.delete(f"auth:{secret}")
        await self.manager.delete(f"auth:code:{email}")
        await self.manager.delete(f"auth:code:{email}:cooldown")
        await self.manager.delete(f"auth:{email}:attempts")

        if password:
            await self.manager.delete(f"auth:password:{email}")

    async def delete_constraint(self, email: str):
        await self.manager.delete(f"auth:code:{email}:cooldown")
        await self.manager.delete(f"auth:{email}:attempts")

    async def set_constraint(self, email: str):

        if await self.manager.keys(f"auth:code:{email}:cooldown"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Cooldown expired"
            )

        await self.manager.set(key=f"auth:code:{email}:cooldown", value="30", ex=30)
        await self.manager.set(key=f"auth:{email}:attempts", value="5", ex=300)

    async def mget(self, values: list[str]):
        return await self.manager.redis.mget(values)

    async def decr(self, key: str, amount: int = 1):
        await self.manager.redis.decr(key, amount)


repo_auth_email = RepositoryAuthEmail(redis_manager)
