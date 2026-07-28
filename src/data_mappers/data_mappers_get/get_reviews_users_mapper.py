from uuid import UUID

from pydantic import BaseModel


class GetReviewUserMapper(BaseModel):
    id: UUID
    nickname: str
