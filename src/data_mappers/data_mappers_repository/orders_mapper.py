from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class OrderMapper(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    delivery_address: str
    delivery_method: str
    total_price: Decimal
