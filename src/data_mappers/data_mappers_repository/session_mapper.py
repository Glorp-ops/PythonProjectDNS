import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SessionMapper(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    auth_ssid: str
    refresh_token: str
    id: str
    user_agent: str
    ip: str
    user_id: UUID
    expires_at: datetime.datetime
    created_at: datetime.datetime
    revoked: bool
    update: bool
