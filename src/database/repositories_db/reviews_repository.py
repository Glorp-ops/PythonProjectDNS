from ...data_mappers.data_mappers_repository import ReviewMapper
from ..db_models import Review
from ..repositories_db import BaseRepository


class ReviewsRepository(BaseRepository):
    model = Review
    mapper = ReviewMapper
