from pydantic import BaseModel

from src.core.config import settings


class TokenInfo(BaseModel):
    access_token: str
    token_type: str = settings.settings_jwt.TYPE_JWT
