from datetime import datetime

from pydantic import BaseModel

from .get_reviews_users_mapper import (
    GetReviewUserMapper,
)


class GetReviewItemMapper(BaseModel):
    id: int
    product_id: int
    rating: float
    content: str
    created_at: datetime
    likes_count: int
    user: GetReviewUserMapper
