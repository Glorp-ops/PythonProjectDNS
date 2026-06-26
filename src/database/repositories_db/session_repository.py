from sqlalchemy.orm import joinedload
from sqlalchemy.sql.expression import select

from src.database.db_models import Session
from src.database.repositories_db.base_repository import BaseRepository
from src.datamapers.session_mapper import SessionMaper


class SessionRepository(BaseRepository):
    mapper = SessionMaper
    model = Session

    async def get_all_join(self):

        sessions_user = await self.session.scalars(
            select(self.model).options(joinedload(self.model.users))
        )

        await self.session.commit()

        return [
            self.schemes.model_validate(session_user) for session_user in sessions_user
        ]
