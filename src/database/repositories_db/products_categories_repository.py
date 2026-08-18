from ...data_mappers.data_mappers_repository import ProductCategoryMapper
from ..db_models import ProductCategory
from .base_repository import BaseRepository


class ProductCategoryRepository(BaseRepository):
    model = ProductCategory
    mapper = ProductCategoryMapper
