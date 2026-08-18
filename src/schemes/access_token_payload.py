from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field


class AccessTokenPayload(BaseModel):
    authSSID: Annotated[str, Field(strict=True)]  # noqa:N815
    jti: UUID
    userId: UUID  # noqa:N815
    userName: Annotated[str | None, Field(strict=True)]  # noqa:N815
    exp: Annotated[int, Field(strict=True)]
    iat: Annotated[int, Field(strict=True)]
    rnd: str
