from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class FavoriteMapper(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    user_id: UUID
    created_at: datetime
