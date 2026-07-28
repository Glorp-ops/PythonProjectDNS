from pydantic import BaseModel


class GetReviewPaginationMapper(BaseModel):
    page: int
    size: int
    pages_all: int
