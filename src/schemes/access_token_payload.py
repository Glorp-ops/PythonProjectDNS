from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field


class AccessTokenPayload(BaseModel):
    authSSID: Annotated[str, Field(strict=True)]
    jti: UUID
    userId: UUID
    userName: Annotated[str | None, Field(strict=True)]
    exp: Annotated[int, Field(strict=True)]
    iat: Annotated[int, Field(strict=True)]
    rnd: str
