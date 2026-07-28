from datetime import datetime

from pydantic import BaseModel

from .get_products_mapper import GetProductsMapper


class GetOrdersScheme(BaseModel):
    id: int
    status: str
    total_price: int
    total_items_count: int
    created_at: datetime
    products: GetProductsMapper
