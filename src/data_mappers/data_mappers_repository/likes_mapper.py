from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class LikeMapper(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: UUID
    review_id: int
    is_like: bool = Field(default=True)
    created_at: datetime
