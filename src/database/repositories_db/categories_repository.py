from ...data_mappers.data_mappers_repository import CategoriesMapper
from ..db_models import Category
from ..repositories_db import BaseRepository


class CategoriesRepository(BaseRepository):
    model = Category
    mapper = CategoriesMapper
