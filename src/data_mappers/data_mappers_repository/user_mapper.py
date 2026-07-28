from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserMapper(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str | None = None
    nickname: str | None = None
    surname: str | None = None
    email: str | None = None
    password: str | None = None
    active_at: bool = True
    is_blocked: bool
