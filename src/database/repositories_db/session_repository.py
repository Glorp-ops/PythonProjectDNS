from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.orm import joinedload

from ...data_mappers.data_mappers_repository import SessionMapper
from ..db_models import Session
from ..repositories_db import BaseRepository


class SessionRepository(BaseRepository):
    mapper = SessionMapper
    model = Session

    async def get_all_join(self):

        sessions_user = await self.session.scalars(
            select(self.model).options(joinedload(self.model.users))
        )

        await self.session.commit()

        return [self.mapper.model_validate(session_user) for session_user in sessions_user]

    async def delete_with_and_not(self, user_id: UUID, auth_public_uid: str):
        smt = (
            delete(self.model)
            .where(self.model.user_id == user_id, self.model.id != auth_public_uid)
            .returning(self.model)
        )

        objects = await self.session.execute(smt)

        await self.session.commit()

        return objects

    async def delete_with_and(self, user_id: UUID, auth_public_uid: str):
        smt = (
            delete(self.model)
            .where(self.model.user_id == user_id, self.model.id == auth_public_uid)
            .returning(self.model)
        )

        objects = await self.session.execute(smt)

        await self.session.commit()

        return objects
