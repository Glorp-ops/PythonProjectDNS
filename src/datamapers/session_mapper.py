import datetime

from pydantic import BaseModel, ConfigDict


class SessionMaper(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    auth_ssid: str
    refresh_token: str
    auth_public_uid: str
    user_agent: str
    ip: str
    expires_at: datetime.datetime
    created_at: datetime.datetime
