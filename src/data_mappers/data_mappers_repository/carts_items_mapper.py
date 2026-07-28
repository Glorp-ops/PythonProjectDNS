from pydantic import BaseModel, ConfigDict


class CartsItemsMapper(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    price_at_add: int
    quantity: int
    total_price: int
