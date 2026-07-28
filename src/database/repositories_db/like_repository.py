from uuid import UUID

from sqlalchemy import func, select

from ...data_mappers.data_mappers_repository import LikeMapper
from ..db_models import Like
from ..repositories_db import BaseRepository


class LikeRepository(BaseRepository):
    mapper = LikeMapper
    model = Like

    async def create_review_like(self, review_id: int, user_id: UUID):
        like = await LikeRepository(self.session).add(review_id=review_id, user_id=user_id)

        like_count = await self.session.scalar(
            select(func.count())
            .where(self.model.review_id == review_id)
            .select_from(self.model)
        )

        return like, like_count
