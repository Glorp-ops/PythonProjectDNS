from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ReviewMapper(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    user_id: UUID
    rating: float
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
