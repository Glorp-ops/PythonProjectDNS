import logging

from pydantic import BaseModel

from src.database.db_models import User
from src.database.repositories_db.base_repository import BaseRepository
from src.datamapers.user_mapper import UserMaper


class UserRepository(BaseRepository):
    model = User
    mapper: BaseModel = UserMaper

    async def check_auth_emai_user(self, nickname: str, email: str):

        user = await UserRepository(self.session).get_filter(email=email)

        logging.info(nickname)

        if not user:
            user_add = await UserRepository(self.session).add(
                email=email, nickname=nickname
            )

            await self.session.commit()

            return user_add

        await self.session.commit()

        return user
