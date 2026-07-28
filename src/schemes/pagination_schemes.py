from typing import Annotated

from fastapi import Depends, Query
from pydantic import BaseModel


class PaginationScheme(BaseModel):
    page: Annotated[int, Query(default=1, ge=0)]
    size: Annotated[int, Query(default=20, ge=0)]


pagination = Annotated[PaginationScheme, Depends()]
