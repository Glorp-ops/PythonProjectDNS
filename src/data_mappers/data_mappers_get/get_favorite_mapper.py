from pydantic import BaseModel, Field

from ..data_mappers_repository import ProductsMapper


class GetFavoriteMapper(BaseModel):
    is_favorite: bool = Field(default=True)
    favorite_id: int
    product: ProductsMapper
