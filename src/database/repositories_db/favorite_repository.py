from ...data_mappers.data_mappers_repository import FavoriteMapper
from ..db_models import Favorite
from ..repositories_db import BaseRepository


class FavoriteRepository(BaseRepository):
    mapper = FavoriteMapper
    model = Favorite
