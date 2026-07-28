from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class OrderItemMapper(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_id: int
    product_id: int
    quantity: int
    price_at_purchase: Decimal
