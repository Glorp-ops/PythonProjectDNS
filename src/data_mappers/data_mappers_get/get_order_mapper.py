from pydantic import BaseModel

from ..data_mappers_repository import ProductsMapper


class GetOrderScheme(BaseModel):
    quantity: int
    price_per_item: int
    total_item_price: int
    product: ProductsMapper
