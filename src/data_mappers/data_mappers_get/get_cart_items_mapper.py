from pydantic import BaseModel

from src.data_mappers.data_mappers_get.get_products_mapper import GetProductsMapper


class GetCartItemsMapper(BaseModel):
    price_at_add: int
    quantity: int
    total_price: int
    product: GetProductsMapper
