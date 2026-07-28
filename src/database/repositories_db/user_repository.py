from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from starlette import status

from ...data_mappers.data_mappers_repository import UserMapper
from ..db_models import User
from ..repositories_db import BaseRepository


class UserRepository(BaseRepository):
    model = User
    mapper = UserMapper

    async def get_filter_with_and_not(self, model_id: UUID, **kwargs):

        smt = select(self.model).filter_by(**kwargs).where(self.model.id != model_id)

        objects = await self.session.execute(smt)

        if objects.scalar_one_or_none() is None:
            return None

        return self.mapper.model_validate(objects.scalar_one_or_none())

    async def check_user_email(self, email: str):
        from src.dependencies.checker import check_active, check_block

        user_email = await UserRepository(self.session).get_filter(email=email)

        if not user_email:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        await check_active(session=self.session, user_id=user_email[0].id)
        await check_block(session=self.session, user_id=user_email[0].id)

        return user_email
