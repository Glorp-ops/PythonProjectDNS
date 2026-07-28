from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CartMapper(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
