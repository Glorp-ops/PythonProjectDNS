from pydantic import BaseModel

from ..core import settings


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int = settings.settings_jwt.EXPIRATION_ACCESS
    token_type: str = settings.settings_jwt.TYPE_JWT
