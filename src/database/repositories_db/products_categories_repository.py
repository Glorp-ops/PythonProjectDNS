from .base_repository import BaseRepository
from ..db_models import ProductCategory
from ...data_mappers.data_mappers_repository import ProductCategoryMapper


class ProductCategoryRepository(BaseRepository):
    model = ProductCategory
    mapper = ProductCategoryMapper
