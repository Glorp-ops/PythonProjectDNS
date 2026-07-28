from datetime import datetime

from pydantic import BaseModel


class BlacklistMapper(BaseModel):
    user_id: int
    reason: str
    ban_until: datetime
    created_at: datetime
