import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ProductsMapper(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    images_url: list[str] | str | None = Field(None)
    name: str
    price: int
    quantity: int
    created_at: datetime.datetime
    is_deleted: bool
    description: str
    review_count: int
    rating: float
    sku: str
    active_at: bool
    created_at: datetime.datetime
    categories: list[int] | None = Field(None)
