from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserMaper(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str | None = None
    nickname: str
    number_phone: str | None = None
    email: str | None = None
    active_at: bool = True
