from datetime import datetime

from pydantic import BaseModel, ConfigDict

from src.data_mappers.data_mappers_get.get_products_mapper import GetProductsMapper


class GetFavoritesMapper(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    favorite_id: int
    added_at: datetime
    products: GetProductsMapper
